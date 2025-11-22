"""
Frontend Engineer Agent

Implements React components, forms, and pages.
"""

from agents.base import AgentInput, AgentOutput, BaseAgent
from orchestrator.core.models import AgentRole, WorkspaceContext


class FrontendEngineerAgent(BaseAgent):
    """Frontend Engineer - Implements React components and pages"""

    def __init__(self):
        super().__init__(role=AgentRole.FRONTEND_ENGINEER, model="claude-sonnet-4.5", temperature=0.1)

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        workspace = input_data.workspace_context
        system_prompt = self.get_system_prompt(workspace)
        user_prompt = self.get_user_prompt(workspace, input_data.previous_deliverables)

        component_code = await self.call_llm(system_prompt, user_prompt)
        component_path = workspace.workspace_path / "05-frontend" / "components" / "feature-component.tsx"
        self.save_file(component_path, component_code)

        deliverable = self.create_deliverable(
            name="React Components",
            deliverable_type="file",
            path=component_path,
            content=component_code,
            metadata={"language": "typescript", "framework": "react"},
        )

        return AgentOutput(deliverables=[deliverable], success=True)

    def get_system_prompt(self, workspace_context: WorkspaceContext) -> str:
        return f"""You are a Frontend Engineer specializing in React and Next.js.

Implement:
- React Server Components (default)
- Client Components ('use client' when needed)
- Forms with react-hook-form + Zod
- Shadcn UI components
- Responsive design (mobile-first)
- TypeScript types

Follow Next.js 16 App Router patterns.

Project: {workspace_context.project_path}"""
