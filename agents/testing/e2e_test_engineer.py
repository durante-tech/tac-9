"""
E2E Test Engineer Agent

Implements Playwright end-to-end tests.
"""

from agents.base import AgentInput, AgentOutput, BaseAgent
from orchestrator.core.models import AgentRole, WorkspaceContext


class E2ETestEngineerAgent(BaseAgent):
    """E2E Test Engineer - Implements Playwright tests"""

    def __init__(self):
        super().__init__(role=AgentRole.E2E_TEST_ENGINEER, model="claude-sonnet-4.5", temperature=0.1)

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        workspace = input_data.workspace_context
        system_prompt = self.get_system_prompt(workspace)
        user_prompt = self.get_user_prompt(workspace, input_data.previous_deliverables)

        e2e_tests = await self.call_llm(system_prompt, user_prompt)
        test_path = workspace.workspace_path / "06-tests" / "e2e" / "feature.spec.ts"
        self.save_file(test_path, e2e_tests)

        deliverable = self.create_deliverable(
            name="E2E Tests",
            deliverable_type="file",
            path=test_path,
            content=e2e_tests,
            metadata={"framework": "playwright", "language": "typescript"},
        )

        return AgentOutput(deliverables=[deliverable], success=True)

    def get_system_prompt(self, workspace_context: WorkspaceContext) -> str:
        return f"""You are an E2E Test Engineer using Playwright.

Write tests that:
- Test complete user flows
- Use data-test attributes for selectors
- Handle authentication
- Test both personal and team accounts
- Validate UI state
- Check accessibility

Project: {workspace_context.project_path}"""
