# Quick Start Guide - TAC-9

Get up and running with TAC-9 in 5 minutes!

## Prerequisites

- Python 3.12+
- `uv` package manager
- API key from OpenAI or Anthropic
- Next.js + Supabase project (to target)

## Installation

```bash
# Clone TAC-9
git clone https://github.com/durante-tech/tac-9.git
cd tac-9

# Install dependencies
uv sync --all-extras

# Copy environment template
cp .env.sample .env
```

## Configuration

Edit `.env`:

```bash
# Required: Add your API key
ANTHROPIC_API_KEY=sk-ant-your-key-here
# OR
OPENAI_API_KEY=sk-your-key-here

# Required: Set your target project
TARGET_PROJECT_PATH=/Users/yourname/Developer/next-supabase-saas-kit-turbo
```

## Your First Feature

### Option 1: Interactive Mode (Recommended)

```bash
uv run tac9 interactive
```

Follow the prompts:

```
📝 What feature would you like to build?
> Add a team activity log showing all member actions

📄 Do you have an existing PRD document? No

Select mode: 1 (Full SDLC)

🚀 Ready to start? Yes
```

The orchestrator will:
1. **Product Phase**: Create PRD with user stories
2. **Architecture Phase**: Design system architecture and database schema
3. **Implementation Phase**: Generate migrations, Server Actions, and React components
4. **Testing Phase**: Create E2E and database tests
5. **Review Phase**: Run security, code, and performance audits
6. **Deployment Phase**: Generate documentation and deployment guide

### Option 2: Command Line

```bash
# Full SDLC from description
uv run tac9 full "Add team activity log with filtering by member and date"

# From existing PRD
uv run tac9 from-prd docs/prd/analytics-feature.md

# Specific agent only
uv run tac9 agent database-engineer "Design schema for file storage system"
```

## Output

After execution, check your workspace:

```bash
cd workspace/feature-team-activity-log/

# View PRD
cat 01-prd/prd.md

# View database migration
cat 03-database/migration.sql

# View Server Actions
cat 04-backend/server-actions.ts

# View React components
cat 05-frontend/components/*.tsx

# View tests
cat 06-tests/e2e/*.spec.ts

# View security audit
cat 07-reviews/security-audit.md

# View documentation
cat 08-docs/README.md
```

## Next Steps

1. **Review Generated Code**: Check all deliverables in the workspace
2. **Run Tests**: Copy tests to your project and run them
3. **Apply Migration**: Run the Supabase migration
4. **Integrate Code**: Copy Server Actions and components to your project
5. **Test Integration**: Verify everything works together

## Tips

- **Start small**: Try a simple feature first
- **Review everything**: Always review generated code before using
- **Iterate**: Re-run specific agents if output needs refinement
- **Check quality gates**: Pay attention to security and performance warnings

## Troubleshooting

**"No API key found"**: Make sure you've set `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` in `.env`

**"Target project not found"**: Verify `TARGET_PROJECT_PATH` points to a valid Next.js project

**"Agent failed"**: Check `logs/conversations/` for detailed agent output

## Examples

See `examples/` directory for:
- `01-team-activity-log/`: Complete activity logging feature
- `02-advanced-analytics/`: Dashboard with charts
- `03-file-uploads/`: File upload system with Supabase Storage

## Learn More

- **Full Documentation**: See `docs/` directory
- **Agent Reference**: See `docs/agents/`
- **Architecture**: See `docs/architecture/`
- **Workflows**: See `workflows/` for different SDLC patterns
