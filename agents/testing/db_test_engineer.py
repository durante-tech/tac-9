"""
DB Test Engineer Agent

Implements pgTAP database tests.
"""

from agents.base import AgentInput, AgentOutput, BaseAgent
from orchestrator.core.models import AgentRole, WorkspaceContext


class DBTestEngineerAgent(BaseAgent):
    """DB Test Engineer - Implements pgTAP tests"""

    def __init__(self):
        super().__init__(role=AgentRole.DB_TEST_ENGINEER, model="claude-sonnet-4.5", temperature=0.1)

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        workspace = input_data.workspace_context
        system_prompt = self.get_system_prompt(workspace)
        user_prompt = self.get_user_prompt(workspace, input_data.previous_deliverables)

        db_tests = await self.call_llm(system_prompt, user_prompt)
        test_path = workspace.workspace_path / "06-tests" / "db" / "feature-tests.sql"
        self.save_file(test_path, db_tests)

        deliverable = self.create_deliverable(
            name="Database Tests",
            deliverable_type="file",
            path=test_path,
            content=db_tests,
            metadata={"framework": "pgtap", "language": "sql"},
        )

        return AgentOutput(deliverables=[deliverable], success=True)

    def get_system_prompt(self, workspace_context: WorkspaceContext) -> str:
        return """You are a Database Test Engineer using pgTAP.

Write tests for:
- RLS policies (can/cannot access data)
- Database functions (correct outputs)
- Triggers (automatic behavior)
- Constraints (validation)
- Permissions

Use pgTAP assertion functions."""
