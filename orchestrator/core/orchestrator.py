"""
Main Orchestrator - Coordinates specialist agents through SDLC workflow
"""

import asyncio
import uuid
from datetime import datetime

from rich.console import Console

from orchestrator.core.config import settings
from orchestrator.core.models import (
    AgentRole,
    AgentStatus,
    AgentTask,
    FeatureRequest,
    SDLCPhase,
    WorkflowExecution,
    WorkflowMode,
    WorkspaceContext,
)

console = Console()


class SDLCOrchestrator:
    """
    Orchestrates specialist agents through the complete SDLC workflow.

    Coordinates 13+ specialist agents working in parallel to deliver
    production-ready features from PRD to deployment.
    """

    def __init__(self):
        self.settings = settings
        self.executions: dict[str, WorkflowExecution] = {}

    async def execute_feature_request(
        self,
        request: FeatureRequest,
        mode: WorkflowMode = WorkflowMode.FULL,
    ) -> WorkflowExecution:
        """
        Execute a complete feature request through the SDLC workflow.

        Args:
            request: Feature request with description and requirements
            mode: Workflow execution mode (full, prd, phase, agent)

        Returns:
            WorkflowExecution with results
        """
        execution_id = str(uuid.uuid4())
        console.print(f"\n[bold cyan]Starting SDLC Orchestration[/bold cyan] (ID: {execution_id})")

        # Create workspace
        workspace = await self._create_workspace(request)
        console.print(f"[green]✓[/green] Workspace created: {workspace.workspace_path}")

        # Create workflow execution
        execution = WorkflowExecution(
            id=execution_id,
            mode=mode,
            feature_request=request,
            workspace_context=workspace,
            status=AgentStatus.RUNNING,
        )
        self.executions[execution_id] = execution

        try:
            # Execute workflow based on mode
            if mode == WorkflowMode.FULL:
                await self._execute_full_workflow(execution)
            elif mode == WorkflowMode.PRD:
                await self._execute_from_prd(execution)
            elif mode == WorkflowMode.PHASE:
                await self._execute_phase(execution, request.metadata.get("phase"))
            elif mode == WorkflowMode.AGENT:
                await self._execute_agent(execution, request.metadata.get("agent"))

            execution.status = AgentStatus.COMPLETED
            execution.completed_at = datetime.now()

            console.print("\n[bold green]✅ SDLC Orchestration Complete![/bold green]")
            self._print_summary(execution)

        except Exception as e:
            execution.status = AgentStatus.FAILED
            execution.error = str(e)
            console.print(f"\n[bold red]❌ Orchestration Failed:[/bold red] {e}")
            raise

        return execution

    async def _execute_full_workflow(self, execution: WorkflowExecution) -> None:
        """Execute the complete SDLC workflow (all phases)"""
        phases = [
            SDLCPhase.PRODUCT,
            SDLCPhase.ARCHITECTURE,
            SDLCPhase.IMPLEMENTATION,
            SDLCPhase.TESTING,
            SDLCPhase.REVIEW,
            SDLCPhase.DEPLOYMENT,
        ]

        for phase in phases:
            if not self._is_phase_enabled(phase):
                console.print(f"[yellow]⊘[/yellow] Phase {phase.value} is disabled, skipping")
                continue

            console.print(f"\n[bold magenta]{'=' * 60}[/bold magenta]")
            console.print(f"[bold magenta]PHASE: {phase.value.upper()}[/bold magenta]")
            console.print(f"[bold magenta]{'=' * 60}[/bold magenta]\n")

            execution.current_phase = phase
            await self._execute_phase_agents(execution, phase)

    async def _execute_from_prd(self, execution: WorkflowExecution) -> None:
        """Execute workflow starting from existing PRD (skip Product phase)"""
        # Load PRD
        prd_path = execution.feature_request.prd_path
        if not prd_path or not prd_path.exists():
            raise ValueError(f"PRD not found: {prd_path}")

        console.print(f"[green]✓[/green] Loading PRD from: {prd_path}")
        # TODO: Load and parse PRD

        # Execute remaining phases
        phases = [
            SDLCPhase.ARCHITECTURE,
            SDLCPhase.IMPLEMENTATION,
            SDLCPhase.TESTING,
            SDLCPhase.REVIEW,
            SDLCPhase.DEPLOYMENT,
        ]

        for phase in phases:
            if not self._is_phase_enabled(phase):
                continue
            execution.current_phase = phase
            await self._execute_phase_agents(execution, phase)

    async def _execute_phase(self, execution: WorkflowExecution, phase: SDLCPhase) -> None:
        """Execute a specific phase only"""
        console.print(f"\n[bold]Executing Phase: {phase.value}[/bold]")
        execution.current_phase = phase
        await self._execute_phase_agents(execution, phase)

    async def _execute_agent(self, execution: WorkflowExecution, agent_role: AgentRole) -> None:
        """Execute a specific agent only"""
        console.print(f"\n[bold]Executing Agent: {agent_role.value}[/bold]")
        task = self._create_agent_task(execution, agent_role)
        await self._run_agent(execution, task)

    async def _execute_phase_agents(self, execution: WorkflowExecution, phase: SDLCPhase) -> None:
        """Execute all agents for a specific phase"""
        agent_roles = self._get_agents_for_phase(phase)

        # Create tasks for all agents in this phase
        tasks = [
            self._create_agent_task(execution, role)
            for role in agent_roles
            if self._is_agent_enabled(role)
        ]

        if not tasks:
            console.print(f"[yellow]No agents enabled for phase {phase.value}[/yellow]")
            return

        # Determine if we can run agents in parallel for this phase
        can_parallelize = phase in [
            SDLCPhase.IMPLEMENTATION,
            SDLCPhase.TESTING,
            SDLCPhase.REVIEW,
        ]

        if can_parallelize and len(tasks) > 1:
            console.print(f"[cyan]⚙️  Running {len(tasks)} agents in parallel...[/cyan]")
            await self._run_agents_parallel(execution, tasks)
        else:
            console.print(f"[cyan]⚙️  Running {len(tasks)} agents sequentially...[/cyan]")
            await self._run_agents_sequential(execution, tasks)

    async def _run_agents_parallel(
        self, execution: WorkflowExecution, tasks: list[AgentTask]
    ) -> None:
        """Run multiple agents in parallel with concurrency limit"""
        semaphore = asyncio.Semaphore(self.settings.max_parallel_agents)

        async def run_with_semaphore(task: AgentTask):
            async with semaphore:
                await self._run_agent(execution, task)

        await asyncio.gather(*[run_with_semaphore(task) for task in tasks])

    async def _run_agents_sequential(
        self, execution: WorkflowExecution, tasks: list[AgentTask]
    ) -> None:
        """Run agents sequentially (one after another)"""
        for task in tasks:
            await self._run_agent(execution, task)

    async def _run_agent(self, execution: WorkflowExecution, task: AgentTask) -> None:
        """Run a single agent task"""
        agent_name = task.agent_role.value
        console.print(f"  [cyan]→[/cyan] Starting {agent_name}...")

        task.status = AgentStatus.RUNNING
        task.started_at = datetime.now()
        execution.add_task(task)

        try:
            # TODO: Load agent and execute
            # For now, simulate agent execution
            await asyncio.sleep(1)  # Simulate work

            task.status = AgentStatus.COMPLETED
            task.completed_at = datetime.now()

            duration = (task.completed_at - task.started_at).total_seconds()
            console.print(f"  [green]✓[/green] {agent_name} completed ({duration:.1f}s)")

        except Exception as e:
            task.status = AgentStatus.FAILED
            task.error = str(e)
            task.completed_at = datetime.now()

            console.print(f"  [red]✗[/red] {agent_name} failed: {e}")

            if task.retry_count < self.settings.agent_max_retries:
                task.retry_count += 1
                console.print(
                    f"  [yellow]↻[/yellow] Retrying {agent_name} "
                    f"({task.retry_count}/{self.settings.agent_max_retries})..."
                )
                task.status = AgentStatus.PENDING
                await self._run_agent(execution, task)
            else:
                raise

    def _create_agent_task(self, execution: WorkflowExecution, agent_role: AgentRole) -> AgentTask:
        """Create a task for an agent"""
        phase = self._get_phase_for_agent(agent_role)
        return AgentTask(
            agent_role=agent_role,
            phase=phase,
            description=f"Execute {agent_role.value} for {execution.workspace_context.feature_name}",
            inputs={
                "workspace_path": str(execution.workspace_context.workspace_path),
                "project_path": str(execution.workspace_context.project_path),
                "feature_request": execution.feature_request.model_dump(),
            },
        )

    async def _create_workspace(self, request: FeatureRequest) -> WorkspaceContext:
        """Create a workspace for the feature"""
        # Generate feature name from description
        feature_name = self._generate_feature_name(request.description)

        # Create workspace directory
        workspace_path = self.settings.workspace_dir / f"feature-{feature_name}"
        workspace_path.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        subdirs = [
            "01-prd",
            "02-architecture",
            "03-database",
            "04-backend",
            "05-frontend",
            "06-tests",
            "07-reviews",
            "08-docs",
        ]
        for subdir in subdirs:
            (workspace_path / subdir).mkdir(exist_ok=True)

        return WorkspaceContext(
            feature_name=feature_name,
            workspace_path=workspace_path,
            project_path=self.settings.target_project_path,
            request=request,
        )

    def _generate_feature_name(self, description: str) -> str:
        """Generate a slug-friendly feature name from description"""
        import re

        name = description.lower()
        name = re.sub(r"[^\w\s-]", "", name)
        name = re.sub(r"[-\s]+", "-", name)
        name = name[:50]  # Limit length
        return name.strip("-")

    def _get_agents_for_phase(self, phase: SDLCPhase) -> list[AgentRole]:
        """Get all agents for a specific phase"""
        phase_agents = {
            SDLCPhase.PRODUCT: [
                AgentRole.PRODUCT_MANAGER,
                AgentRole.UX_RESEARCHER,
                AgentRole.BUSINESS_ANALYST,
            ],
            SDLCPhase.ARCHITECTURE: [
                AgentRole.SOLUTIONS_ARCHITECT,
                AgentRole.DATABASE_ARCHITECT,
                AgentRole.SECURITY_ARCHITECT,
            ],
            SDLCPhase.IMPLEMENTATION: [
                AgentRole.DATABASE_ENGINEER,
                AgentRole.BACKEND_ENGINEER,
                AgentRole.FRONTEND_ENGINEER,
            ],
            SDLCPhase.TESTING: [
                AgentRole.QA_ENGINEER,
                AgentRole.E2E_TEST_ENGINEER,
                AgentRole.DB_TEST_ENGINEER,
            ],
            SDLCPhase.REVIEW: [
                AgentRole.SECURITY_ENGINEER,
                AgentRole.CODE_REVIEWER,
                AgentRole.PERFORMANCE_ENGINEER,
            ],
            SDLCPhase.DEPLOYMENT: [
                AgentRole.TECHNICAL_WRITER,
                AgentRole.DEVOPS_ENGINEER,
            ],
        }
        return phase_agents.get(phase, [])

    def _get_phase_for_agent(self, agent_role: AgentRole) -> SDLCPhase:
        """Get the phase for a specific agent"""
        for phase in SDLCPhase:
            if agent_role in self._get_agents_for_phase(phase):
                return phase
        raise ValueError(f"Unknown agent role: {agent_role}")

    def _is_phase_enabled(self, phase: SDLCPhase) -> bool:
        """Check if a phase is enabled"""
        phase_settings = {
            SDLCPhase.PRODUCT: self.settings.enable_product_phase,
            SDLCPhase.ARCHITECTURE: self.settings.enable_architecture_phase,
            SDLCPhase.IMPLEMENTATION: self.settings.enable_implementation_phase,
            SDLCPhase.TESTING: self.settings.enable_testing_phase,
            SDLCPhase.REVIEW: self.settings.enable_review_phase,
            SDLCPhase.DEPLOYMENT: self.settings.enable_deployment_phase,
        }
        return phase_settings.get(phase, True)

    def _is_agent_enabled(self, agent_role: AgentRole) -> bool:
        """Check if an agent is enabled"""
        agent_settings = {
            AgentRole.PRODUCT_MANAGER: self.settings.enable_product_manager,
            AgentRole.SOLUTIONS_ARCHITECT: self.settings.enable_solutions_architect,
            AgentRole.DATABASE_ARCHITECT: self.settings.enable_database_architect,
            AgentRole.DATABASE_ENGINEER: self.settings.enable_database_engineer,
            AgentRole.BACKEND_ENGINEER: self.settings.enable_backend_engineer,
            AgentRole.FRONTEND_ENGINEER: self.settings.enable_frontend_engineer,
            AgentRole.E2E_TEST_ENGINEER: self.settings.enable_e2e_test_engineer,
            AgentRole.DB_TEST_ENGINEER: self.settings.enable_db_test_engineer,
            AgentRole.SECURITY_ENGINEER: self.settings.enable_security_engineer,
            AgentRole.CODE_REVIEWER: self.settings.enable_code_reviewer,
            AgentRole.PERFORMANCE_ENGINEER: self.settings.enable_performance_engineer,
            AgentRole.TECHNICAL_WRITER: self.settings.enable_technical_writer,
            AgentRole.DEVOPS_ENGINEER: self.settings.enable_devops_engineer,
        }
        return agent_settings.get(agent_role, True)

    def _print_summary(self, execution: WorkflowExecution) -> None:
        """Print execution summary"""
        console.print("\n[bold]Execution Summary:[/bold]")
        console.print(f"  Feature: {execution.workspace_context.feature_name}")
        console.print(f"  Workspace: {execution.workspace_context.workspace_path}")

        duration = (execution.completed_at - execution.started_at).total_seconds()
        console.print(f"  Duration: {duration:.1f}s")

        total_tasks = len(execution.tasks)
        completed = len(execution.get_tasks_by_status(AgentStatus.COMPLETED))
        failed = len(execution.get_tasks_by_status(AgentStatus.FAILED))

        console.print(f"  Tasks: {completed}/{total_tasks} completed, {failed} failed")

        if execution.workspace_context.deliverables:
            console.print(f"  Deliverables: {len(execution.workspace_context.deliverables)}")

        if execution.workspace_context.quality_gates:
            passed_gates = sum(1 for g in execution.workspace_context.quality_gates if g.passed)
            total_gates = len(execution.workspace_context.quality_gates)
            console.print(f"  Quality Gates: {passed_gates}/{total_gates} passed")
