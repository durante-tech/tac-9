"""
Database Engineer Agent

Implements database migrations, RLS policies, and functions.
"""

from agents.base import AgentInput, AgentOutput, BaseAgent
from orchestrator.core.models import AgentRole, WorkspaceContext


class DatabaseEngineerAgent(BaseAgent):
    """Database Engineer - Implements migrations and RLS policies"""

    def __init__(self):
        super().__init__(role=AgentRole.DATABASE_ENGINEER, model="claude-sonnet-4.5", temperature=0.1)

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        workspace = input_data.workspace_context
        system_prompt = self.get_system_prompt(workspace)
        user_prompt = self.get_user_prompt(workspace, input_data.previous_deliverables)

        migration_sql = await self.call_llm(system_prompt, user_prompt)
        migration_path = workspace.workspace_path / "03-database" / "migration.sql"
        self.save_file(migration_path, migration_sql)

        deliverable = self.create_deliverable(
            name="Supabase Migration",
            deliverable_type="file",
            path=migration_path,
            content=migration_sql,
            metadata={"type": "sql", "database": "postgresql"},
        )

        return AgentOutput(deliverables=[deliverable], success=True)

    def get_system_prompt(self, workspace_context: WorkspaceContext) -> str:
        return f"""You are a Database Engineer specializing in Supabase/PostgreSQL.

Create production-ready SQL migrations with:
- CREATE TABLE statements
- Indexes for performance
- RLS policies (ENABLE ROW LEVEL SECURITY)
- Database functions (PL/pgSQL)
- Triggers for automation
- Foreign key constraints

Project: {workspace_context.project_path}

Follow Supabase migration patterns. Use gen_random_uuid() for IDs."""
