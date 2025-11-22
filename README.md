# TAC-9: Agentic SDLC Orchestrator

**From Idea to Production-Ready Feature in Minutes, Not Days**

TAC-9 is an advanced multi-agent system that orchestrates the complete Software Development Life Cycle (SDLC) for Next.js + Supabase applications. It takes a feature idea or PRD and coordinates 13 specialized AI agents to deliver production-ready code with database schemas, server actions, React components, comprehensive tests, and documentation.

---

## 🎯 What is TAC-9?

TAC-9 represents the pinnacle of the TAC framework: **fully automated, production-grade feature development**. It combines all previous TAC concepts—agentic prompting (TAC-1), context engineering (TAC-2), full-stack development (TAC-3), AI workflows (TAC-4/5), multi-agent orchestration (TAC-6), and real-time observability (TAC-7)—into a unified SDLC orchestrator.

### The Problem

Building a single feature in a modern full-stack SaaS application requires:
- **Product thinking**: Understanding user needs, writing PRDs, defining acceptance criteria
- **Architecture design**: System design, database schema, API design
- **Implementation**: Database migrations, RLS policies, server actions, React components
- **Testing**: E2E tests (Playwright), database tests (pgTAP), integration tests
- **Security review**: RLS validation, input sanitization, vulnerability scanning
- **Code review**: TypeScript quality, React best practices, performance optimization
- **Documentation**: API docs, user guides, inline comments
- **Deployment**: Migration planning, environment setup, CI/CD integration

This typically takes a team of engineers **days to weeks** and requires expertise across multiple domains.

### The TAC-9 Solution

TAC-9 orchestrates **13 specialized AI agents** working in parallel to complete all SDLC phases:

```
Feature Idea → [TAC-9 Orchestrator] → Production-Ready Feature
                     ↓
    ┌────────────────┼────────────────┐
    │                │                │
Product Team    Implementation    Quality & Deploy
    │                │                │
    ↓                ↓                ↓
PRD + Specs    Code + Tests    Docs + Deploy
```

**Time to production**: Minutes to hours (vs. days to weeks)

---

## 🤖 The 13 Specialist Agents

### Phase 1: Product Definition
1. **Product Manager Agent** - Converts ideas into comprehensive PRDs
2. **UX Researcher Agent** - Analyzes user flows and personas
3. **Business Analyst Agent** - Defines acceptance criteria and metrics

### Phase 2: Architecture & Design
4. **Solutions Architect Agent** - Designs system architecture
5. **Database Architect Agent** - Designs schema, RLS, and functions
6. **Security Architect Agent** - Defines security model

### Phase 3: Parallel Implementation
7. **Database Engineer Agent** - Creates migrations, RLS, functions
8. **Backend Engineer Agent** - Builds server actions, services, schemas
9. **Frontend Engineer Agent** - Builds React components, forms, pages

### Phase 4: Quality Assurance
10. **QA Engineer Agent** - Defines test strategy
11. **E2E Test Engineer Agent** - Writes Playwright tests
12. **Database Test Engineer Agent** - Writes pgTAP tests

### Phase 5: Security & Review
13. **Security Engineer Agent** - Security audit and vulnerability scanning
14. **Code Reviewer Agent** - Code quality and best practices
15. **Performance Engineer Agent** - Performance analysis

### Phase 6: Documentation & Deployment
16. **Technical Writer Agent** - API docs, user guides, README
17. **DevOps Engineer Agent** - Deployment pipeline, migrations

---

## 🏗️ Architecture

### Stack-Specific Expertise

TAC-9 is **deeply specialized** for the Next.js + Supabase + Turborepo stack:

- **Next.js 16 App Router**: Server Components, Server Actions, streaming
- **Supabase**: PostgreSQL, Row Level Security (RLS), database functions
- **Turborepo**: Monorepo with shared packages
- **TypeScript**: Full type safety with generated types
- **Tailwind + Shadcn UI**: Component library patterns
- **React Hook Form + Zod**: Form validation patterns
- **Playwright**: E2E testing with auth flows
- **pgTAP**: Database testing framework

### Orchestration Patterns

**Sequential Phases** (Phase 1-2):
```
Product Manager → UX Researcher → Business Analyst →
Solutions Architect → Database Architect → Security Architect
```

**Parallel Implementation** (Phase 3):
```
        ┌─→ Database Engineer
Spec ───┼─→ Backend Engineer
        └─→ Frontend Engineer
```

**Parallel Testing** (Phase 4):
```
        ┌─→ E2E Test Engineer
Code ───┼─→ Database Test Engineer
        └─→ Integration Test Engineer
```

**Parallel Review** (Phase 5):
```
         ┌─→ Security Engineer
Tests ───┼─→ Code Reviewer
         └─→ Performance Engineer
```

### Workspace Structure

Each feature gets an isolated workspace:

```
workspace/feature-{name}/
├── 01-prd/
│   ├── prd.md                    # Product requirements
│   └── user-stories.md           # Acceptance criteria
├── 02-architecture/
│   ├── system-design.md          # Architecture overview
│   ├── component-diagram.mmd     # Component relationships
│   └── data-flow.mmd             # Data flow diagrams
├── 03-database/
│   ├── migration.sql             # Supabase migration
│   ├── rls-policies.sql          # Row Level Security
│   ├── functions.sql             # Database functions
│   └── tests.sql                 # pgTAP tests
├── 04-backend/
│   ├── schemas.ts                # Zod validation schemas
│   ├── server-actions.ts         # Next.js Server Actions
│   ├── service.ts                # Service layer
│   └── loaders.ts                # Data loaders
├── 05-frontend/
│   ├── components/               # React components
│   ├── pages/                    # Page components
│   └── forms/                    # Form components
├── 06-tests/
│   ├── e2e/                      # Playwright tests
│   └── db/                       # pgTAP tests
├── 07-reviews/
│   ├── security-audit.md         # Security report
│   ├── code-review.md            # Code quality report
│   └── performance-audit.md      # Performance report
└── 08-docs/
    ├── README.md                 # Feature documentation
    ├── api-reference.md          # API documentation
    └── user-guide.md             # User documentation
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+** (with `uv` package manager)
- **Node.js 20+** (with `pnpm`)
- **Supabase CLI** (for local development)
- **Next.js + Supabase SaaS application** (target codebase)
- **API Keys**: OpenAI or Anthropic (for AI agents)

### Installation

```bash
# Clone TAC-9
cd ~/Developer/tac
git clone https://github.com/durante-tech/tac-9.git

# Navigate to TAC-9
cd tac-9

# Install Python dependencies
uv sync --all-extras

# Copy environment template
cp .env.sample .env

# Configure API keys and target project
vim .env
```

### Configuration

Edit `.env` with your settings:

```bash
# AI Provider (choose one or both)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Target Project (Next.js + Supabase SaaS Kit)
TARGET_PROJECT_PATH=/path/to/next-supabase-saas-kit-turbo

# Supabase Configuration
SUPABASE_URL=http://localhost:54321
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# GitHub (optional - for PR automation)
GITHUB_TOKEN=ghp_...

# Orchestrator Settings
MAX_PARALLEL_AGENTS=3
AGENT_TIMEOUT_SECONDS=600
ENABLE_AUTO_COMMIT=false
ENABLE_AUTO_PR=false
```

### Run Your First Feature

```bash
# Start the orchestrator
uv run python orchestrator/main.py

# Or use the interactive CLI
uv run python orchestrator/cli.py
```

**Example Session:**

```
╭─ TAC-9: Agentic SDLC Orchestrator ─╮
│  From Idea to Production in Minutes │
╰─────────────────────────────────────╯

📝 Describe your feature (or provide PRD path):
> Add a team activity log that shows all actions taken by team members
> with filtering by member, date range, and activity type

🤖 Analyzing feature requirements...

✓ Product Manager Agent: PRD created
✓ Solutions Architect: System design complete
✓ Database Architect: Schema designed

⚙️  Parallel Implementation (3 agents)...
  ├─ Database Engineer: Migration created
  ├─ Backend Engineer: Server actions created
  └─ Frontend Engineer: Components created

✅ Testing (2 agents)...
  ├─ E2E Test Engineer: 8 tests created
  └─ DB Test Engineer: 12 policy tests created

🔒 Security & Review (3 agents)...
  ├─ Security Engineer: No vulnerabilities found
  ├─ Code Reviewer: All checks passed
  └─ Performance Engineer: Bundle impact +12KB (acceptable)

📚 Documentation (1 agent)...
  └─ Technical Writer: Docs generated

🚀 Ready to deploy!

📂 Workspace: workspace/feature-team-activity-log/
🎫 Create GitHub PR? (y/n):
```

---

## 📋 Usage Patterns

### 1. Full SDLC (PRD → Production)

**Input**: Feature idea or problem statement

```bash
uv run python orchestrator/cli.py --mode full --feature "User onboarding wizard"
```

**Output**:
- Complete PRD with user stories
- Database migration with RLS policies
- Server actions and services
- React components and pages
- E2E and database tests
- Security and code review reports
- Documentation
- GitHub PR (optional)

---

### 2. From Existing PRD

**Input**: PRD document (Markdown, Google Docs, Notion)

```bash
uv run python orchestrator/cli.py --mode prd --prd-path docs/prd/advanced-analytics.md
```

**Output**:
- Skips Product phase
- Goes directly to Architecture → Implementation → Testing → Review

---

### 3. Incremental (Specific Phases)

**Input**: Existing code + specific phase

```bash
# Only run testing phase (add tests to existing feature)
uv run python orchestrator/cli.py --mode phase --phase testing --feature-path packages/features/analytics

# Only run security review
uv run python orchestrator/cli.py --mode phase --phase security --feature-path packages/features/analytics
```

---

### 4. Agent-Specific Tasks

**Input**: Specific agent + task

```bash
# Run only Database Architect to design schema
uv run python orchestrator/cli.py --agent database-architect --task "Design schema for multi-tenant file storage"

# Run only Security Engineer to audit existing feature
uv run python orchestrator/cli.py --agent security-engineer --audit packages/features/billing
```

---

## 🛠️ Agent Configuration

Each agent can be customized via `agents/{category}/{agent}/config.yaml`:

```yaml
# agents/implementation/database-engineer/config.yaml
name: database-engineer
display_name: Database Engineer
category: implementation
model: claude-sonnet-4.5  # or gpt-4o
temperature: 0.1           # Low for code generation
max_tokens: 16000

stack_expertise:
  - postgresql
  - supabase
  - row-level-security
  - pgtap
  - database-functions

deliverables:
  - migration.sql
  - rls-policies.sql
  - functions.sql
  - tests.sql

quality_gates:
  - migration_valid: true
  - rls_policies_secure: true
  - functions_tested: true
  - types_generated: true

templates:
  migration: templates/database/migration.sql.j2
  rls_policy: templates/database/rls-policy.sql.j2
  function: templates/database/function.sql.j2
  test: templates/database/test.sql.j2
```

---

## 🧪 Examples

TAC-9 includes complete examples:

### Example 1: Team Activity Log

**Feature**: Track all team member actions with filtering

**Demonstrates**:
- Multi-tenant data design
- RLS policies with team isolation
- Server actions with pagination
- React table with filtering
- E2E tests with test data
- Performance optimization (database indexes)

**Location**: `examples/01-team-activity-log/`

**Run**:
```bash
cd examples/01-team-activity-log
uv run python ../../orchestrator/cli.py --config example-config.yaml
```

---

### Example 2: Advanced Analytics Dashboard

**Feature**: Recharts dashboard with real-time metrics

**Demonstrates**:
- Database views for analytics
- Scheduled jobs (pg_cron)
- Real-time subscriptions
- Chart components
- Performance optimization (materialized views)

**Location**: `examples/02-advanced-analytics/`

---

### Example 3: File Upload System

**Feature**: Multi-tenant file uploads with Supabase Storage

**Demonstrates**:
- Storage bucket policies
- File upload components
- Presigned URLs
- File type validation
- Security scanning

**Location**: `examples/03-file-uploads/`

---

## 📊 Deliverables

TAC-9 generates production-ready artifacts:

### Database Artifacts
- ✅ Supabase migrations (`{timestamp}_{feature}.sql`)
- ✅ Row Level Security (RLS) policies
- ✅ Database functions (PL/pgSQL)
- ✅ Triggers (timestamps, validation)
- ✅ Indexes (performance optimization)
- ✅ pgTAP tests (policy validation)
- ✅ Generated TypeScript types

### Backend Artifacts
- ✅ Zod validation schemas
- ✅ Next.js Server Actions
- ✅ Service layer (business logic)
- ✅ Data loaders (for pages)
- ✅ API routes (webhooks, if needed)
- ✅ Error handling
- ✅ Logging integration

### Frontend Artifacts
- ✅ React Server Components (pages)
- ✅ React Client Components (interactive)
- ✅ Forms with react-hook-form + Zod
- ✅ Shadcn UI components (tables, dialogs)
- ✅ Layouts and loading states
- ✅ i18n translations
- ✅ Responsive design

### Testing Artifacts
- ✅ Playwright E2E tests
- ✅ Test fixtures and factories
- ✅ pgTAP database tests
- ✅ Test data seeds
- ✅ Test documentation

### Documentation Artifacts
- ✅ Feature README
- ✅ API reference
- ✅ User guide
- ✅ Inline JSDoc comments
- ✅ Architecture diagrams (Mermaid)
- ✅ Migration guide (if breaking changes)

### Review Artifacts
- ✅ Security audit report
- ✅ Code review report
- ✅ Performance analysis
- ✅ Bundle size impact
- ✅ Remediation recommendations

---

## 🎓 Learning Path

TAC-9 builds on all previous TAC levels. **Recommended progression**:

1. **TAC-1** - Agent basics and tool use
2. **TAC-2** - Context engineering and memory management
3. **TAC-3** - Full-stack development (base application)
4. **TAC-4** - AI Developer Workflows (ADW)
5. **TAC-5** - GitHub automation and worktree isolation
6. **TAC-6** - Multi-agent orchestration
7. **TAC-7** - Real-time observability with hooks
8. **TAC-8** - Meta-platform integration
9. **TAC-9** - Complete SDLC orchestration ← You are here

**Educational Modules**:
- **Agentic Prompt Engineering** (APE) - Foundation for agent design
- **Building Specialized Agents** (BSA) - Domain-specific agent patterns
- **Elite Context Engineering** (ECE) - Advanced context management
- **Multi-Agent Orchestration** (MAO) - Agent coordination patterns

---

## 🔧 Development

### Project Structure

```
tac-9/
├── orchestrator/          # Core orchestration engine
│   ├── core/             # Orchestrator core logic
│   ├── services/         # Agent services
│   ├── api/              # REST API (optional)
│   └── utils/            # Shared utilities
├── agents/               # Agent definitions
│   ├── product/          # Product phase agents
│   ├── architecture/     # Architecture phase agents
│   ├── implementation/   # Implementation phase agents
│   ├── testing/          # Testing phase agents
│   ├── review/           # Review phase agents
│   └── deployment/       # Deployment phase agents
├── workflows/            # Workflow definitions
│   ├── full-sdlc.yaml   # Complete SDLC workflow
│   ├── implementation-only.yaml
│   └── testing-only.yaml
├── templates/            # Code generation templates
│   ├── database/         # SQL templates
│   ├── backend/          # TypeScript backend templates
│   ├── frontend/         # React component templates
│   └── tests/            # Test templates
├── workspace/            # Feature workspaces (git-ignored)
├── examples/             # Example features
├── docs/                 # Documentation
│   ├── agents/           # Agent documentation
│   ├── workflows/        # Workflow guides
│   └── architecture/     # System architecture
├── scripts/              # Utility scripts
├── tests/                # Orchestrator tests
└── .claude/              # Claude Code integration
    ├── commands/         # Slash commands
    └── hooks/            # Event hooks
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test suite
uv run pytest tests/agents/test_database_engineer.py

# Run with coverage
uv run pytest --cov=orchestrator --cov=agents

# Run integration tests (requires target project)
uv run pytest tests/integration/ --target-project=/path/to/project
```

### Adding New Agents

```bash
# Use the agent generator
uv run python scripts/generate_agent.py \
  --name "integration-test-engineer" \
  --category "testing" \
  --expertise "jest,vitest,integration-testing" \
  --deliverables "integration-tests.ts"

# Edit generated files
vim agents/testing/integration-test-engineer/agent.py
vim agents/testing/integration-test-engineer/config.yaml
vim agents/testing/integration-test-engineer/prompts/system.md

# Test the agent
uv run python tests/agents/test_integration_test_engineer.py
```

---

## 🤝 Contributing

TAC-9 is part of the TAC (Tactical Agentic Coding) framework. Contributions welcome!

**How to contribute**:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-agent`)
3. Add your agent or workflow
4. Add tests and documentation
5. Submit a pull request

**Agent contribution checklist**:
- [ ] Agent config (`config.yaml`)
- [ ] Agent implementation (`agent.py`)
- [ ] System prompt (`prompts/system.md`)
- [ ] Templates (if applicable)
- [ ] Unit tests
- [ ] Integration test
- [ ] Documentation (`README.md`)
- [ ] Example usage

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---

## 🙏 Acknowledgments

TAC-9 is inspired by:
- **Anthropic's Claude** - Advanced AI capabilities
- **Vercel's v0** - AI-powered UI generation
- **Cursor AI** - AI pair programming
- **GitHub Copilot** - Code assistance
- **Devin by Cognition** - Autonomous software engineer

TAC-9 combines the best ideas from these tools into a **stack-specific, production-ready SDLC orchestrator**.

---

## 🔗 Resources

- **TAC Repository**: https://github.com/durante-tech/tac
- **Next.js Supabase SaaS Kit**: https://makerkit.dev
- **Documentation**: https://tac.dev
- **Community Discord**: https://discord.gg/tac
- **YouTube Channel**: TAC Framework Tutorials

---

## 📞 Support

- **Issues**: https://github.com/durante-tech/tac-9/issues
- **Discussions**: https://github.com/durante-tech/tac-9/discussions
- **Email**: support@tac.dev
- **Twitter**: @tac_framework

---

**Built with ❤️ by the TAC community**

*Making AI-assisted development accessible, predictable, and production-ready.*
