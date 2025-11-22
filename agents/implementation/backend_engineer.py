"""
Backend Engineer Agent

Implements Server Actions, services, and Zod schemas.
"""

from agents.base import AgentInput, AgentOutput, BaseAgent
from orchestrator.core.models import AgentRole, WorkspaceContext


class BackendEngineerAgent(BaseAgent):
    """Backend Engineer - Implements Server Actions and services"""

    def __init__(self):
        super().__init__(role=AgentRole.BACKEND_ENGINEER, model="claude-sonnet-4.5", temperature=0.1)

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        workspace = input_data.workspace_context
        system_prompt = self.get_system_prompt(workspace)
        user_prompt = self.get_user_prompt(workspace, input_data.previous_deliverables)

        backend_code = await self.call_llm(system_prompt, user_prompt)
        backend_path = workspace.workspace_path / "04-backend" / "server-actions.ts"
        self.save_file(backend_path, backend_code)

        deliverable = self.create_deliverable(
            name="Server Actions",
            deliverable_type="file",
            path=backend_path,
            content=backend_code,
            metadata={"language": "typescript", "type": "server-actions"},
        )

        return AgentOutput(deliverables=[deliverable], success=True)

    def get_system_prompt(self, workspace_context: WorkspaceContext) -> str:
        return f"""You are a Backend Engineer for Next.js applications.

Implement:
- Next.js Server Actions with 'use server'
- Zod validation schemas
- Service layer with Supabase client
- Error handling
- Type-safe code

Use patterns:
- enhanceAction() wrapper
- getSupabaseServerClient()
- Proper TypeScript types

Project: {workspace_context.project_path}"""
