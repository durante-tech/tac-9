# CLAUDE.md - TAC-9 Integration Guide

This file provides guidance to Claude Code (claude.ai/code) when working with the TAC-9 Agentic SDLC Orchestrator.

## Project Overview

TAC-9 is an advanced multi-agent orchestration system that coordinates 13+ specialist AI agents through a complete Software Development Life Cycle (SDLC) workflow. It takes a feature idea or PRD and delivers production-ready code for Next.js + Supabase applications.

## Architecture

### Core Components

- **Orchestrator** (`orchestrator/`): Core engine that coordinates agent execution
- **Agents** (`agents/`): 13+ specialist agents (Product Manager, Database Engineer, etc.)
- **Workflows** (`workflows/`): YAML configurations for different SDLC patterns
- **Templates** (`templates/`): Jinja2 templates for code generation
- **Workspace** (`workspace/`): Ephemeral workspaces for feature development (git-ignored)

### Technology Stack

- **Python 3.12+**: Core orchestrator and agents
- **uv**: Fast Python package manager
- **Pydantic**: Data validation and settings
- **Rich**: Terminal UI and progress tracking
- **Typer**: CLI framework
- **Jinja2**: Template engine
- **Anthropic/OpenAI**: AI model providers

## Development Workflow

### Running the Orchestrator

```bash
# Interactive mode (recommended for first-time users)
uv run tac9 interactive

# Full SDLC from description
uv run tac9 full "Add team activity log feature"

# From existing PRD
uv run tac9 from-prd docs/prd/analytics.md

# Specific agent only
uv run tac9 agent database-engineer "Design schema for file storage"

# List all available agents
uv run tac9 list-agents

# Show current configuration
uv run tac9 config
```

### Common Tasks

**Add a new specialist agent:**
```bash
# 1. Create agent file in appropriate category
vim agents/{category}/{agent_name}.py

# 2. Inherit from BaseAgent
# 3. Implement execute() and get_system_prompt()
# 4. Add agent to orchestrator agent mapping
# 5. Add config setting in Settings class
# 6. Write tests
uv run pytest tests/agents/test_{agent_name}.py
```

**Create a new workflow:**
```bash
# 1. Create YAML file in workflows/
vim workflows/my-workflow.yaml

# 2. Define phases, agents, and quality gates
# 3. Test workflow
uv run python tests/test_workflows.py
```

**Modify templates:**
```bash
# Templates use Jinja2 syntax
vim templates/{category}/{template_name}.j2
```

### Testing

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/orchestrator/test_orchestrator.py

# Run with coverage
uv run pytest --cov=orchestrator --cov=agents

# Run integration tests (requires target project)
TARGET_PROJECT_PATH=/path/to/nextjs-app uv run pytest tests/integration/
```

### Code Quality

```bash
# Format code
uv run black .

# Lint
uv run ruff check .

# Type check
uv run mypy orchestrator/ agents/
```

## Key Design Patterns

### 1. Agent Pattern

All specialist agents inherit from `BaseAgent`:

```python
from agents.base import AgentInput, AgentOutput, BaseAgent
from orchestrator.core.models import AgentRole

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role=AgentRole.MY_AGENT,
            model="claude-sonnet-4.5",
            temperature=0.1
        )

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        # 1. Get prompts
        system_prompt = self.get_system_prompt(input_data.workspace_context)
        user_prompt = self.get_user_prompt(...)

        # 2. Call LLM
        result = await self.call_llm(system_prompt, user_prompt)

        # 3. Save deliverables
        path = workspace.workspace_path / "output.md"
        self.save_file(path, result)

        # 4. Create deliverable
        deliverable = self.create_deliverable(...)

        # 5. Return output
        return AgentOutput(deliverables=[deliverable], success=True)
```

### 2. Parallel Execution Pattern

The orchestrator runs agents in parallel when possible:

```python
# Implementation, Testing, and Review phases run agents in parallel
# Other phases (Product, Architecture) run sequentially

can_parallelize = phase in [
    SDLCPhase.IMPLEMENTATION,
    SDLCPhase.TESTING,
    SDLCPhase.REVIEW,
]
```

### 3. Workspace Pattern

Each feature gets an isolated workspace:

```
workspace/feature-{name}/
├── 01-prd/              # Product phase outputs
├── 02-architecture/     # Architecture phase outputs
├── 03-database/         # Database artifacts
├── 04-backend/          # Backend code
├── 05-frontend/         # Frontend code
├── 06-tests/            # Test files
├── 07-reviews/          # Review reports
└── 08-docs/             # Documentation
```

### 4. Quality Gate Pattern

Agents produce quality gates to validate their work:

```python
quality_gate = self.create_quality_gate(
    name="Security Audit",
    passed=not has_vulnerabilities,
    message="No critical vulnerabilities found",
    details={"vulnerabilities": []}
)
```

## Configuration

### Environment Variables

Copy `.env.sample` to `.env` and configure:

```bash
# Required: At least one AI provider
ANTHROPIC_API_KEY=sk-ant-...
# or
OPENAI_API_KEY=sk-...

# Required: Target project path
TARGET_PROJECT_PATH=/path/to/next-supabase-app

# Optional: Supabase (for database operations)
SUPABASE_URL=http://localhost:54321
SUPABASE_SERVICE_ROLE_KEY=...

# Optional: GitHub (for PR automation)
GITHUB_TOKEN=ghp_...
GITHUB_REPO=owner/repo

# Orchestrator settings
MAX_PARALLEL_AGENTS=3
AGENT_TIMEOUT_SECONDS=600
```

### Agent Configuration

Each agent can be individually enabled/disabled:

```bash
ENABLE_PRODUCT_MANAGER=true
ENABLE_DATABASE_ENGINEER=true
ENABLE_FRONTEND_ENGINEER=true
# ... etc
```

### Workflow Configuration

Workflows are defined in YAML:

```yaml
name: My Workflow
phases:
  - implementation
  - testing

agents:
  implementation:
    - database-engineer
    - backend-engineer
    execution: parallel
```

## Troubleshooting

### Agent Fails to Execute

1. Check agent implementation has `execute()` method
2. Verify system prompt is well-formed
3. Check API keys are valid
4. Review agent logs in `logs/conversations/`

### Workspace Not Created

1. Ensure `WORKSPACE_DIR` exists and is writable
2. Check disk space
3. Verify permissions

### Tests Failing

1. Ensure target project path is correct
2. Check all dependencies installed: `uv sync --all-extras`
3. Verify API keys for integration tests

### Performance Issues

1. Reduce `MAX_PARALLEL_AGENTS` if hitting rate limits
2. Use `gpt-4o-mini` or `claude-haiku` for faster agents
3. Enable streaming: `ENABLE_STREAMING=true`

## Best Practices

1. **Start with Product Phase**: Always run Product phase first for new features
2. **Use Quality Gates**: Enable quality gates to catch issues early
3. **Review Deliverables**: Check workspace outputs before committing
4. **Iterate on Prompts**: Agent effectiveness depends on prompt quality
5. **Test Integration**: Run integration tests before deploying agents
6. **Monitor Costs**: Track API usage with multiple agents running

## Integration with Parent TAC Repository

TAC-9 is part of the larger TAC (Tactical Agentic Coding) framework:

- **TAC-1 to TAC-8**: Progressive learning path for agentic coding
- **TAC-9**: Production SDLC orchestrator (this project)
- **Educational modules**: APE, BSA, ECE, MAO

To use TAC-9 with the parent repository:

```bash
# From parent TAC repo
cd ~/Developer/tac
git submodule add https://github.com/durante-tech/tac-9.git tac-9
git submodule update --init --recursive
```

## Contributing

When adding new agents or features:

1. Create feature branch
2. Implement agent following `BaseAgent` pattern
3. Add tests (unit + integration)
4. Update documentation
5. Submit PR with example usage

## Resources

- **Main README**: Comprehensive overview and usage guide
- **Agent Documentation**: See `agents/{category}/README.md`
- **Workflow Examples**: See `workflows/`
- **Templates**: See `templates/`
- **Tests**: See `tests/` for examples

## Important Notes

- Agents are **stateless**: Each execution is independent
- Workspaces are **ephemeral**: Clean up old workspaces regularly
- Quality gates are **critical**: Don't disable without good reason
- Parallel execution requires **sufficient API quota**
- Always **review generated code** before committing

For questions or issues, see GitHub Issues or Discussions.
