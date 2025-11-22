"""
Solutions Architect Agent

Designs system architecture, component interactions, and data flow.
"""

from agents.base import AgentInput, AgentOutput, BaseAgent
from orchestrator.core.models import AgentRole, WorkspaceContext


class SolutionsArchitectAgent(BaseAgent):
    """Solutions Architect - Designs overall system architecture"""

    def __init__(self):
        super().__init__(role=AgentRole.SOLUTIONS_ARCHITECT, model="claude-sonnet-4.5", temperature=0.1)

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        workspace = input_data.workspace_context
        system_prompt = self.get_system_prompt(workspace)
        user_prompt = self.get_user_prompt(workspace, input_data.previous_deliverables)

        architecture_doc = await self.call_llm(system_prompt, user_prompt)
        arch_path = workspace.workspace_path / "02-architecture" / "system-design.md"
        self.save_file(arch_path, architecture_doc)

        deliverable = self.create_deliverable(
            name="System Architecture Design",
            deliverable_type="document",
            path=arch_path,
            content=architecture_doc,
        )

        return AgentOutput(deliverables=[deliverable], success=True)

    def get_system_prompt(self, workspace_context: WorkspaceContext) -> str:
        return f"""You are a Solutions Architect for Next.js + Supabase applications.

Design:
- Component hierarchy (Server Components, Client Components)
- Data flow (loaders → components → actions)
- Package structure (which packages affected)
- API design (Server Actions vs API routes)
- State management patterns

Project: {workspace_context.project_path}

Create architecture design with Mermaid diagrams."""
