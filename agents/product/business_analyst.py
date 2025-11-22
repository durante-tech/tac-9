"""
Business Analyst Agent

Defines acceptance criteria, success metrics, and business requirements.
"""

from agents.base import AgentInput, AgentOutput, BaseAgent
from orchestrator.core.models import AgentRole, WorkspaceContext


class BusinessAnalystAgent(BaseAgent):
    """Business Analyst - Defines acceptance criteria and success metrics"""

    def __init__(self):
        super().__init__(role=AgentRole.BUSINESS_ANALYST, model="claude-sonnet-4.5", temperature=0.2)

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        workspace = input_data.workspace_context
        system_prompt = self.get_system_prompt(workspace)
        user_prompt = self.get_user_prompt(workspace, input_data.previous_deliverables)

        acceptance_doc = await self.call_llm(system_prompt, user_prompt)
        doc_path = workspace.workspace_path / "01-prd" / "acceptance-criteria.md"
        self.save_file(doc_path, acceptance_doc)

        deliverable = self.create_deliverable(
            name="Acceptance Criteria & Success Metrics",
            deliverable_type="document",
            path=doc_path,
            content=acceptance_doc,
        )

        return AgentOutput(deliverables=[deliverable], success=True)

    def get_system_prompt(self, workspace_context: WorkspaceContext) -> str:
        return """You are a Business Analyst for SaaS products.

Define:
- Detailed acceptance criteria (Given/When/Then format)
- Success metrics (quantitative and qualitative)
- Business rules and constraints
- Edge cases and error scenarios

Create comprehensive acceptance criteria."""
