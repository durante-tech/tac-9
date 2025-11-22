"""
Base Agent - Foundation for all specialist agents
"""

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from orchestrator.core.models import AgentRole, Deliverable, QualityGate, WorkspaceContext


class AgentInput(BaseModel):
    """Input data for an agent"""

    workspace_context: WorkspaceContext
    previous_deliverables: List[Deliverable] = []
    metadata: Dict[str, Any] = {}


class AgentOutput(BaseModel):
    """Output data from an agent"""

    deliverables: List[Deliverable] = []
    quality_gates: List[QualityGate] = []
    metadata: Dict[str, Any] = {}
    success: bool = True
    error: Optional[str] = None


class BaseAgent(ABC):
    """
    Base class for all specialist agents in TAC-9.

    Each specialist agent:
    - Has deep expertise in a specific domain (e.g., database design, React)
    - Produces specific deliverables (e.g., migrations, components)
    - Validates output with quality gates
    - Integrates with the Next.js + Supabase stack
    """

    def __init__(
        self,
        role: AgentRole,
        model: str = "claude-sonnet-4.5",
        temperature: float = 0.1,
    ):
        self.role = role
        self.model = model
        self.temperature = temperature

    @abstractmethod
    async def execute(self, input_data: AgentInput) -> AgentOutput:
        """
        Execute the agent's task.

        Args:
            input_data: Input containing workspace context and previous deliverables

        Returns:
            AgentOutput with deliverables, quality gates, and metadata
        """
        pass

    @abstractmethod
    def get_system_prompt(self, workspace_context: WorkspaceContext) -> str:
        """
        Get the system prompt for this agent.

        Args:
            workspace_context: Current workspace context

        Returns:
            System prompt string with agent expertise and instructions
        """
        pass

    def get_user_prompt(
        self, workspace_context: WorkspaceContext, previous_deliverables: List[Deliverable]
    ) -> str:
        """
        Get the user prompt for this agent (can be overridden).

        Args:
            workspace_context: Current workspace context
            previous_deliverables: Deliverables from previous agents

        Returns:
            User prompt string with specific task instructions
        """
        return f"""
Execute your role for this feature:

Feature: {workspace_context.feature_name}
Description: {workspace_context.request.description}

Workspace: {workspace_context.workspace_path}
Target Project: {workspace_context.project_path}

Please produce your deliverables according to your role and expertise.
"""

    def create_deliverable(
        self,
        name: str,
        deliverable_type: str,
        path: Path,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Deliverable:
        """Helper to create a deliverable"""
        return Deliverable(
            name=name,
            type=deliverable_type,
            path=path,
            content=content,
            metadata=metadata or {},
            created_by=self.role,
            created_at=datetime.now(),
        )

    def create_quality_gate(
        self,
        name: str,
        passed: bool,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> QualityGate:
        """Helper to create a quality gate"""
        return QualityGate(
            name=name,
            passed=passed,
            message=message,
            details=details or {},
        )

    async def call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """
        Call the LLM with the given prompts.

        Args:
            system_prompt: System prompt
            user_prompt: User prompt

        Returns:
            LLM response text
        """
        # TODO: Implement LLM call based on self.model
        # For now, return a placeholder
        return f"[Placeholder response from {self.model}]"

    def save_file(self, path: Path, content: str) -> None:
        """Save content to a file"""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def read_file(self, path: Path) -> str:
        """Read content from a file"""
        return path.read_text(encoding="utf-8")
