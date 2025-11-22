"""
Security Architect Agent

Defines security model, authentication, authorization, and data protection.
"""

from agents.base import AgentInput, AgentOutput, BaseAgent
from orchestrator.core.models import AgentRole, WorkspaceContext


class SecurityArchitectAgent(BaseAgent):
    """Security Architect - Defines security model and policies"""

    def __init__(self):
        super().__init__(role=AgentRole.SECURITY_ARCHITECT, model="claude-sonnet-4.5", temperature=0.1)

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        workspace = input_data.workspace_context
        system_prompt = self.get_system_prompt(workspace)
        user_prompt = self.get_user_prompt(workspace, input_data.previous_deliverables)

        security_model = await self.call_llm(system_prompt, user_prompt)
        security_path = workspace.workspace_path / "02-architecture" / "security-model.md"
        self.save_file(security_path, security_model)

        deliverable = self.create_deliverable(
            name="Security Model",
            deliverable_type="document",
            path=security_path,
            content=security_model,
        )

        return AgentOutput(deliverables=[deliverable], success=True)

    def get_system_prompt(self, workspace_context: WorkspaceContext) -> str:
        return """You are a Security Architect for SaaS applications.

Define:
- Authentication requirements
- Authorization model (RBAC, permissions)
- RLS policies for data isolation
- Input validation requirements
- OWASP Top 10 mitigations
- Sensitive data handling
- Audit logging requirements

Create comprehensive security model."""
