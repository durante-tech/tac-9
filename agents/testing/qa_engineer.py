"""
QA Engineer Agent

Defines test strategy and coordinates testing efforts.
"""

from agents.base import AgentInput, AgentOutput, BaseAgent
from orchestrator.core.models import AgentRole, WorkspaceContext


class QAEngineerAgent(BaseAgent):
    """QA Engineer - Defines test strategy"""

    def __init__(self):
        super().__init__(role=AgentRole.QA_ENGINEER, model="claude-sonnet-4.5", temperature=0.2)

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        workspace = input_data.workspace_context
        system_prompt = self.get_system_prompt(workspace)
        user_prompt = self.get_user_prompt(workspace, input_data.previous_deliverables)

        test_plan = await self.call_llm(system_prompt, user_prompt)
        plan_path = workspace.workspace_path / "06-tests" / "test-plan.md"
        self.save_file(plan_path, test_plan)

        deliverable = self.create_deliverable(
            name="Test Plan",
            deliverable_type="document",
            path=plan_path,
            content=test_plan,
        )

        return AgentOutput(deliverables=[deliverable], success=True)

    def get_system_prompt(self, workspace_context: WorkspaceContext) -> str:
        return """You are a QA Engineer for SaaS applications.

Define:
- Test scenarios (happy path + edge cases)
- E2E test coverage
- Database test coverage
- Test data requirements
- Acceptance criteria validation

Create comprehensive test plan."""
