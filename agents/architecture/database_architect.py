"""
Database Architect Agent

Designs database schema, RLS policies, and data model.
"""

from agents.base import AgentInput, AgentOutput, BaseAgent
from orchestrator.core.models import AgentRole, WorkspaceContext


class DatabaseArchitectAgent(BaseAgent):
    """Database Architect - Designs database schema and RLS policies"""

    def __init__(self):
        super().__init__(role=AgentRole.DATABASE_ARCHITECT, model="claude-sonnet-4.5", temperature=0.1)

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        workspace = input_data.workspace_context
        system_prompt = self.get_system_prompt(workspace)
        user_prompt = self.get_user_prompt(workspace, input_data.previous_deliverables)

        db_design = await self.call_llm(system_prompt, user_prompt)
        design_path = workspace.workspace_path / "02-architecture" / "database-design.md"
        self.save_file(design_path, db_design)

        deliverable = self.create_deliverable(
            name="Database Schema Design",
            deliverable_type="document",
            path=design_path,
            content=db_design,
        )

        return AgentOutput(deliverables=[deliverable], success=True)

    def get_system_prompt(self, workspace_context: WorkspaceContext) -> str:
        return """You are a Database Architect specializing in PostgreSQL and Supabase.

Design:
- Table schemas with proper types and constraints
- Indexes for performance
- RLS policies for multi-tenant data isolation
- Database functions for business logic
- Triggers for automation
- Foreign keys and relationships

Focus on security, performance, and data integrity."""
