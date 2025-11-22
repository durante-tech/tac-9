"""
UX Researcher Agent

Analyzes user flows, personas, and interaction patterns for features.
"""

from agents.base import AgentInput, AgentOutput, BaseAgent
from orchestrator.core.models import AgentRole, WorkspaceContext


class UXResearcherAgent(BaseAgent):
    """UX Researcher - Analyzes user experience and interaction patterns"""

    def __init__(self):
        super().__init__(role=AgentRole.UX_RESEARCHER, model="claude-sonnet-4.5", temperature=0.3)

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        workspace = input_data.workspace_context
        system_prompt = self.get_system_prompt(workspace)
        user_prompt = self.get_user_prompt(workspace, input_data.previous_deliverables)

        ux_analysis = await self.call_llm(system_prompt, user_prompt)
        analysis_path = workspace.workspace_path / "01-prd" / "ux-analysis.md"
        self.save_file(analysis_path, ux_analysis)

        deliverable = self.create_deliverable(
            name="UX Analysis",
            deliverable_type="document",
            path=analysis_path,
            content=ux_analysis,
        )

        return AgentOutput(deliverables=[deliverable], success=True)

    def get_system_prompt(self, workspace_context: WorkspaceContext) -> str:
        return """You are a UX Researcher specializing in SaaS applications.

Analyze user flows, personas, and interaction patterns. Consider:
- User journey mapping
- Mobile and desktop experiences
- Accessibility requirements
- Multi-tenant UX patterns (personal vs team accounts)

Create a comprehensive UX analysis document."""
