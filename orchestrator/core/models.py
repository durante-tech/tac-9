"""
Data models for TAC-9 Orchestrator
"""

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class SDLCPhase(str, Enum):
    """SDLC Phase enumeration"""

    PRODUCT = "product"
    ARCHITECTURE = "architecture"
    IMPLEMENTATION = "implementation"
    TESTING = "testing"
    REVIEW = "review"
    DEPLOYMENT = "deployment"


class AgentRole(str, Enum):
    """Agent role enumeration"""

    # Product Phase
    PRODUCT_MANAGER = "product-manager"
    UX_RESEARCHER = "ux-researcher"
    BUSINESS_ANALYST = "business-analyst"

    # Architecture Phase
    SOLUTIONS_ARCHITECT = "solutions-architect"
    DATABASE_ARCHITECT = "database-architect"
    SECURITY_ARCHITECT = "security-architect"

    # Implementation Phase
    DATABASE_ENGINEER = "database-engineer"
    BACKEND_ENGINEER = "backend-engineer"
    FRONTEND_ENGINEER = "frontend-engineer"

    # Testing Phase
    QA_ENGINEER = "qa-engineer"
    E2E_TEST_ENGINEER = "e2e-test-engineer"
    DB_TEST_ENGINEER = "db-test-engineer"

    # Review Phase
    SECURITY_ENGINEER = "security-engineer"
    CODE_REVIEWER = "code-reviewer"
    PERFORMANCE_ENGINEER = "performance-engineer"

    # Deployment Phase
    TECHNICAL_WRITER = "technical-writer"
    DEVOPS_ENGINEER = "devops-engineer"


class AgentStatus(str, Enum):
    """Agent execution status"""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class WorkflowMode(str, Enum):
    """Workflow execution mode"""

    FULL = "full"  # Complete SDLC
    PRD = "prd"  # Start from existing PRD
    PHASE = "phase"  # Specific phase only
    AGENT = "agent"  # Specific agent only


class FeatureRequest(BaseModel):
    """Feature request from user"""

    description: str = Field(..., description="Feature description or idea")
    prd_path: Path | None = Field(None, description="Path to existing PRD")
    user_stories: list[str] | None = Field(None, description="User stories")
    acceptance_criteria: list[str] | None = Field(None, description="Acceptance criteria")
    target_package: str | None = Field(
        None, description="Target package (e.g., packages/features/analytics)"
    )
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class AgentTask(BaseModel):
    """Task assigned to an agent"""

    agent_role: AgentRole
    phase: SDLCPhase
    description: str
    inputs: dict[str, Any] = Field(default_factory=dict)
    outputs: dict[str, Any] = Field(default_factory=dict)
    status: AgentStatus = AgentStatus.PENDING
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error: str | None = None
    retry_count: int = 0


class Deliverable(BaseModel):
    """Deliverable produced by an agent"""

    name: str
    type: str  # "file", "document", "report", etc.
    path: Path
    content: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_by: AgentRole
    created_at: datetime = Field(default_factory=datetime.now)


class QualityGate(BaseModel):
    """Quality gate check result"""

    name: str
    passed: bool
    message: str
    details: dict[str, Any] = Field(default_factory=dict)


class WorkspaceContext(BaseModel):
    """Shared context for a feature workspace"""

    feature_name: str
    workspace_path: Path
    project_path: Path
    request: FeatureRequest
    prd: dict[str, Any] | None = None
    architecture: dict[str, Any] | None = None
    deliverables: list[Deliverable] = Field(default_factory=list)
    quality_gates: list[QualityGate] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def add_deliverable(self, deliverable: Deliverable) -> None:
        """Add a deliverable to the workspace"""
        self.deliverables.append(deliverable)
        self.updated_at = datetime.now()

    def add_quality_gate(self, gate: QualityGate) -> None:
        """Add a quality gate result"""
        self.quality_gates.append(gate)
        self.updated_at = datetime.now()

    def get_deliverables_by_agent(self, agent_role: AgentRole) -> list[Deliverable]:
        """Get all deliverables created by a specific agent"""
        return [d for d in self.deliverables if d.created_by == agent_role]

    def has_failed_quality_gates(self) -> bool:
        """Check if any quality gates failed"""
        return any(not gate.passed for gate in self.quality_gates)


class WorkflowExecution(BaseModel):
    """Represents a complete workflow execution"""

    id: str
    mode: WorkflowMode
    feature_request: FeatureRequest
    workspace_context: WorkspaceContext
    tasks: list[AgentTask] = Field(default_factory=list)
    current_phase: SDLCPhase | None = None
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: datetime | None = None
    status: AgentStatus = AgentStatus.PENDING
    error: str | None = None

    def add_task(self, task: AgentTask) -> None:
        """Add a task to the workflow"""
        self.tasks.append(task)

    def get_tasks_by_phase(self, phase: SDLCPhase) -> list[AgentTask]:
        """Get all tasks for a specific phase"""
        return [t for t in self.tasks if t.phase == phase]

    def get_tasks_by_status(self, status: AgentStatus) -> list[AgentTask]:
        """Get all tasks with a specific status"""
        return [t for t in self.tasks if t.status == status]

    def is_phase_complete(self, phase: SDLCPhase) -> bool:
        """Check if a phase is complete"""
        phase_tasks = self.get_tasks_by_phase(phase)
        if not phase_tasks:
            return False
        return all(t.status in [AgentStatus.COMPLETED, AgentStatus.SKIPPED] for t in phase_tasks)

    def has_failed_tasks(self) -> bool:
        """Check if any tasks failed"""
        return any(t.status == AgentStatus.FAILED for t in self.tasks)


class AgentConfig(BaseModel):
    """Configuration for a specialist agent"""

    name: str
    display_name: str
    role: AgentRole
    phase: SDLCPhase
    model: str = "claude-sonnet-4.5"
    temperature: float = 0.1
    max_tokens: int = 64000
    stack_expertise: list[str] = Field(default_factory=list)
    deliverables: list[str] = Field(default_factory=list)
    dependencies: list[AgentRole] = Field(default_factory=list)
    quality_gates: list[str] = Field(default_factory=list)
    templates: dict[str, str] = Field(default_factory=dict)
    enabled: bool = True


class WorkflowConfig(BaseModel):
    """Configuration for a workflow"""

    name: str
    description: str
    phases: list[SDLCPhase]
    agents: list[AgentRole]
    parallel_execution: bool = True
    max_parallel_agents: int = 3
    quality_gates_required: bool = True
    auto_commit: bool = False
    auto_pr: bool = False
