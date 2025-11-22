"""
DevOps Engineer Agent

Plans deployment, migrations, and CI/CD integration.
"""

from agents.base import AgentInput, AgentOutput, BaseAgent
from orchestrator.core.models import AgentRole, WorkspaceContext


class DevOpsEngineerAgent(BaseAgent):
    """DevOps Engineer - Plans deployment"""

    def __init__(self):
        super().__init__(role=AgentRole.DEVOPS_ENGINEER, model="claude-sonnet-4.5", temperature=0.1)

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        workspace = input_data.workspace_context
        system_prompt = self.get_system_prompt(workspace)
        user_prompt = self.get_user_prompt(workspace, input_data.previous_deliverables)

        deployment_plan = await self.call_llm(system_prompt, user_prompt)
        deploy_path = workspace.workspace_path / "08-docs" / "deployment-guide.md"
        self.save_file(deploy_path, deployment_plan)

        deliverable = self.create_deliverable(
            name="Deployment Guide",
            deliverable_type="document",
            path=deploy_path,
            content=deployment_plan,
        )

        return AgentOutput(deliverables=[deliverable], success=True)

    def get_system_prompt(self, workspace_context: WorkspaceContext) -> str:
        return """You are a DevOps Engineer.

Plan:
- Database migration strategy
- Environment variables needed
- CI/CD pipeline updates
- Rollback procedures
- Monitoring setup
- Deployment checklist

Create deployment guide."""
