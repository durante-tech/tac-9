"""
Technical Writer Agent

Generates documentation, API references, and user guides.
"""

from agents.base import AgentInput, AgentOutput, BaseAgent
from orchestrator.core.models import AgentRole, WorkspaceContext


class TechnicalWriterAgent(BaseAgent):
    """Technical Writer - Generates documentation"""

    def __init__(self):
        super().__init__(role=AgentRole.TECHNICAL_WRITER, model="claude-sonnet-4.5", temperature=0.2)

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        workspace = input_data.workspace_context
        system_prompt = self.get_system_prompt(workspace)
        user_prompt = self.get_user_prompt(workspace, input_data.previous_deliverables)

        documentation = await self.call_llm(system_prompt, user_prompt)
        doc_path = workspace.workspace_path / "08-docs" / "README.md"
        self.save_file(doc_path, documentation)

        deliverable = self.create_deliverable(
            name="Feature Documentation",
            deliverable_type="document",
            path=doc_path,
            content=documentation,
        )

        return AgentOutput(deliverables=[deliverable], success=True)

    def get_system_prompt(self, workspace_context: WorkspaceContext) -> str:
        return """You are a Technical Writer for developer documentation.

Create:
- Feature overview
- API reference (Server Actions, types)
- Usage examples
- Configuration guide
- Troubleshooting tips

Write clear, concise documentation."""
