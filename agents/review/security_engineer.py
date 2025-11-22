"""
Security Engineer Agent

Performs security audit and vulnerability scanning.
"""

from agents.base import AgentInput, AgentOutput, BaseAgent
from orchestrator.core.models import AgentRole, WorkspaceContext


class SecurityEngineerAgent(BaseAgent):
    """Security Engineer - Performs security audits"""

    def __init__(self):
        super().__init__(role=AgentRole.SECURITY_ENGINEER, model="claude-sonnet-4.5", temperature=0.1)

    async def execute(self, input_data: AgentInput) -> AgentOutput:
        workspace = input_data.workspace_context
        system_prompt = self.get_system_prompt(workspace)
        user_prompt = self.get_user_prompt(workspace, input_data.previous_deliverables)

        security_audit = await self.call_llm(system_prompt, user_prompt)
        audit_path = workspace.workspace_path / "07-reviews" / "security-audit.md"
        self.save_file(audit_path, security_audit)

        deliverable = self.create_deliverable(
            name="Security Audit Report",
            deliverable_type="document",
            path=audit_path,
            content=security_audit,
        )

        # Check for critical vulnerabilities
        has_vulnerabilities = "CRITICAL" in security_audit or "HIGH" in security_audit
        quality_gate = self.create_quality_gate(
            name="Security Audit",
            passed=not has_vulnerabilities,
            message="No critical vulnerabilities found" if not has_vulnerabilities else "Critical vulnerabilities detected",
        )

        return AgentOutput(deliverables=[deliverable], quality_gates=[quality_gate], success=True)

    def get_system_prompt(self, workspace_context: WorkspaceContext) -> str:
        return """You are a Security Engineer specializing in web application security.

Audit for:
- SQL injection vulnerabilities
- XSS vulnerabilities
- CSRF protection
- RLS policy bypasses
- Input validation gaps
- Secrets exposure
- Authentication/authorization flaws

Generate security audit report with severity ratings."""
