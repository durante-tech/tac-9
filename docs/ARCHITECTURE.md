# TAC-9 Architecture

Comprehensive architectural overview of the Agentic SDLC Orchestrator.

## System Overview

TAC-9 is a multi-agent orchestration system that coordinates specialist AI agents through a complete SDLC workflow to deliver production-ready features for Next.js + Supabase applications.

## Core Components

### 1. Orchestrator (`orchestrator/`)

The central coordination engine that manages agent execution, workflow state, and quality gates.

**Key Classes:**

- `SDLCOrchestrator`: Main orchestrator class
- `WorkflowExecution`: Represents a complete workflow run
- `WorkspaceContext`: Shared state for feature development
- `Settings`: Configuration management

**Responsibilities:**

- Agent lifecycle management
- Parallel execution coordination
- Quality gate enforcement
- Workspace creation and management
- Error handling and retries

### 2. Agents (`agents/`)

13+ specialist agents organized by SDLC phase:

```
agents/
├── product/              # Product Definition Phase
│   ├── product_manager.py
│   ├── ux_researcher.py
│   └── business_analyst.py
├── architecture/         # Architecture & Design Phase
│   ├── solutions_architect.py
│   ├── database_architect.py
│   └── security_architect.py
├── implementation/       # Implementation Phase
│   ├── database_engineer.py
│   ├── backend_engineer.py
│   └── frontend_engineer.py
├── testing/              # Testing Phase
│   ├── qa_engineer.py
│   ├── e2e_test_engineer.py
│   └── db_test_engineer.py
├── review/               # Review Phase
│   ├── security_engineer.py
│   ├── code_reviewer.py
│   └── performance_engineer.py
└── deployment/           # Deployment Phase
    ├── technical_writer.py
    └── devops_engineer.py
```

**Agent Base Class:**

All agents inherit from `BaseAgent`:

```python
class BaseAgent(ABC):
    async def execute(self, input_data: AgentInput) -> AgentOutput
    def get_system_prompt(self, workspace_context: WorkspaceContext) -> str
    def get_user_prompt(self, workspace_context, deliverables) -> str
    async def call_llm(self, system_prompt, user_prompt) -> str
```

### 3. Workflows (`workflows/`)

YAML-based workflow definitions:

- `full-sdlc.yaml`: Complete end-to-end workflow
- `implementation-only.yaml`: Skip planning, go straight to code
- `testing-only.yaml`: Add tests to existing features

**Workflow Structure:**

```yaml
phases:
  - product
  - architecture
  - implementation

agents:
  implementation:
    - database-engineer
    - backend-engineer
    - frontend-engineer
    execution: parallel  # or sequential
    max_parallel: 3

quality_gates:
  - name: Tests Pass
    phase: testing
    type: test_execution
```

### 4. Templates (`templates/`)

Jinja2 code generation templates:

- `database/migration.sql.j2`: Supabase migrations
- `backend/server-actions.ts.j2`: Next.js Server Actions
- `backend/schema.ts.j2`: Zod validation schemas
- `frontend/component.tsx.j2`: React components
- `frontend/form.tsx.j2`: Form components
- `tests/e2e.spec.ts.j2`: Playwright tests

### 5. Workspace (`workspace/`)

Ephemeral workspaces for feature development:

```
workspace/feature-{name}/
├── 01-prd/              # Product phase deliverables
├── 02-architecture/     # Architecture designs
├── 03-database/         # SQL migrations and tests
├── 04-backend/          # Server Actions and services
├── 05-frontend/         # React components
├── 06-tests/            # E2E and DB tests
├── 07-reviews/          # Security and code reviews
└── 08-docs/             # Documentation
```

## Execution Flow

### 1. Workflow Initialization

```
User Request → Feature Request Model → Workspace Creation → Workflow Execution
```

### 2. Phase Execution

For each phase:

1. **Determine agents**: Get agents for current phase
2. **Check if enabled**: Skip disabled agents
3. **Create tasks**: Create `AgentTask` for each agent
4. **Parallel or sequential**: Decide based on phase
5. **Execute agents**: Run with concurrency control
6. **Collect deliverables**: Save to workspace
7. **Validate quality gates**: Check requirements

### 3. Agent Execution

For each agent:

```python
1. Load workspace context
2. Get previous deliverables
3. Build system prompt (agent expertise)
4. Build user prompt (specific task)
5. Call LLM
6. Parse response
7. Save deliverables to workspace
8. Create quality gates
9. Return AgentOutput
```

### 4. Parallel Execution

Implementation, Testing, and Review phases support parallel execution:

```python
async def _run_agents_parallel(self, tasks):
    semaphore = asyncio.Semaphore(max_parallel_agents)

    async def run_with_semaphore(task):
        async with semaphore:
            await self._run_agent(task)

    await asyncio.gather(*[run_with_semaphore(t) for t in tasks])
```

## Data Flow

### Input Flow

```
Feature Description
    ↓
FeatureRequest
    ↓
WorkspaceContext (created)
    ↓
AgentInput (for each agent)
    ↓
Agent Execution
```

### Output Flow

```
Agent Execution
    ↓
AgentOutput (deliverables + quality gates)
    ↓
WorkspaceContext (updated)
    ↓
WorkflowExecution (final result)
```

## State Management

### Workspace Context

Shared state across all agents:

```python
class WorkspaceContext:
    feature_name: str
    workspace_path: Path
    project_path: Path
    request: FeatureRequest
    prd: Optional[Dict]
    architecture: Optional[Dict]
    deliverables: List[Deliverable]
    quality_gates: List[QualityGate]
    metadata: Dict[str, Any]
```

### Workflow Execution

Tracks overall workflow state:

```python
class WorkflowExecution:
    id: str
    mode: WorkflowMode
    feature_request: FeatureRequest
    workspace_context: WorkspaceContext
    tasks: List[AgentTask]
    current_phase: Optional[SDLCPhase]
    status: AgentStatus
```

## Quality Gates

Quality gates validate deliverables:

```python
class QualityGate:
    name: str
    passed: bool
    message: str
    details: Dict[str, Any]
```

**Built-in Gates:**

- PRD Completeness
- Architecture Review
- Code Compiles
- Tests Pass
- Security Audit
- Performance Check

## Error Handling

### Retry Logic

Failed agents are retried up to `AGENT_MAX_RETRIES` times:

```python
if task.retry_count < settings.agent_max_retries:
    task.retry_count += 1
    task.status = AgentStatus.PENDING
    await self._run_agent(execution, task)
```

### Graceful Degradation

- Failed agents don't block subsequent phases
- Quality gate failures are reported but configurable
- Partial workspace outputs are preserved

## Performance Optimizations

1. **Parallel Execution**: Multiple agents run simultaneously
2. **Streaming**: LLM responses streamed for faster feedback
3. **Caching**: Agent conversations cached for debugging
4. **Async I/O**: All I/O operations are async
5. **Concurrency Control**: Semaphore limits parallel agents

## Security Considerations

1. **API Key Management**: Loaded from environment only
2. **Workspace Isolation**: Each feature gets isolated workspace
3. **RLS Awareness**: Agents generate RLS-compliant SQL
4. **Input Validation**: All inputs validated with Pydantic
5. **Security Agent**: Dedicated agent for vulnerability scanning

## Extensibility

### Adding New Agents

1. Create agent file in appropriate phase directory
2. Inherit from `BaseAgent`
3. Implement `execute()` and `get_system_prompt()`
4. Add to orchestrator's agent mapping
5. Add config setting
6. Write tests

### Adding New Workflows

1. Create YAML file in `workflows/`
2. Define phases and agents
3. Configure execution mode (parallel/sequential)
4. Add quality gates
5. Test workflow

### Adding New Templates

1. Create Jinja2 template in `templates/`
2. Define template variables
3. Update agent to use template
4. Test template rendering

## Monitoring & Observability

- **Logs**: Structured logs in `logs/`
- **Conversations**: Agent conversations saved for debugging
- **Quality Gates**: Track validation results
- **Metrics**: Task execution times, success rates

## Dependencies

**Core:**
- `pydantic`: Data validation
- `typer`: CLI framework
- `rich`: Terminal UI
- `jinja2`: Template engine

**AI:**
- `anthropic`: Claude API
- `openai`: OpenAI API

**Async:**
- `asyncio`: Async execution
- `aiofiles`: Async file I/O

## Future Enhancements

- [ ] Real-time UI dashboard
- [ ] Agent performance analytics
- [ ] Custom agent creation wizard
- [ ] Workflow visualization
- [ ] Multi-project support
- [ ] Collaborative workspaces
- [ ] Version control integration
- [ ] CI/CD pipeline automation
