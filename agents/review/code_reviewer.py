"""
Code Reviewer Agent

Performs code quality review and best practices check.
"""

from agents.base import AgentInput, AgentOutput, BaseAgent
from orchestrator.core.models import AgentRole, WorkspaceContext


class CodeReviewerAgent(BaseAgent):
    """Code Reviewer - Reviews code quality and best practices"""

    def __init__(self):
        super().__init__(role=AgentRole.CODE_REVIEWER, model="claude-sonnet-4.5", temperature=0.1)

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        workspace = input_data.workspace_context
        system_prompt = self.get_system_prompt(workspace)
        user_prompt = self.get_user_prompt(workspace, input_data.previous_deliverables)

        code_review = await self.call_llm(system_prompt, user_prompt)
        review_path = workspace.workspace_path / "07-reviews" / "code-review.md"
        self.save_file(review_path, code_review)

        deliverable = self.create_deliverable(
            name="Code Review Report",
            deliverable_type="document",
            path=review_path,
            content=code_review,
        )

        return AgentOutput(deliverables=[deliverable], success=True)

    def get_system_prompt(self, workspace_context: WorkspaceContext) -> str:
        return """You are a Senior Code Reviewer.

Review for:
- TypeScript best practices
- React patterns (hooks, components)
- Next.js optimization
- Code duplication
- Naming conventions
- Error handling
- Code maintainability

Provide constructive feedback."""
