"""
Performance Engineer Agent

Analyzes performance and provides optimization recommendations.
"""

from agents.base import AgentInput, AgentOutput, BaseAgent
from orchestrator.core.models import AgentRole, WorkspaceContext


class PerformanceEngineerAgent(BaseAgent):
    """Performance Engineer - Analyzes performance"""

    def __init__(self):
        super().__init__(role=AgentRole.PERFORMANCE_ENGINEER, model="claude-sonnet-4.5", temperature=0.1)

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        workspace = input_data.workspace_context
        system_prompt = self.get_system_prompt(workspace)
        user_prompt = self.get_user_prompt(workspace, input_data.previous_deliverables)

        perf_analysis = await self.call_llm(system_prompt, user_prompt)
        perf_path = workspace.workspace_path / "07-reviews" / "performance-audit.md"
        self.save_file(perf_path, perf_analysis)

        deliverable = self.create_deliverable(
            name="Performance Analysis",
            deliverable_type="document",
            path=perf_path,
            content=perf_analysis,
        )

        return AgentOutput(deliverables=[deliverable], success=True)

    def get_system_prompt(self, workspace_context: WorkspaceContext) -> str:
        return """You are a Performance Engineer.

Analyze:
- Bundle size impact
- Database query optimization
- N+1 query problems
- Missing database indexes
- Unnecessary re-renders
- Core Web Vitals impact

Provide optimization recommendations."""
