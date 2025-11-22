"""
TAC-9 Command Line Interface

Interactive CLI for the Agentic SDLC Orchestrator
"""

import asyncio
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

from orchestrator.core.config import settings
from orchestrator.core.models import FeatureRequest, WorkflowMode
from orchestrator.core.orchestrator import SDLCOrchestrator

app = typer.Typer(
    name="tac9",
    help="TAC-9: Agentic SDLC Orchestrator - From Idea to Production in Minutes",
    add_completion=False,
)
console = Console()


def print_banner():
    """Print TAC-9 banner"""
    banner = """
╭─────────────────────────────────────────────────────╮
│                                                     │
│      TAC-9: Agentic SDLC Orchestrator              │
│      From Idea to Production in Minutes            │
│                                                     │
╰─────────────────────────────────────────────────────╯
"""
    console.print(Panel(banner, style="bold cyan"))


@app.command()
def interactive():
    """
    Start interactive mode - walk through feature creation step by step
    """
    print_banner()

    console.print("\n[bold]Welcome to TAC-9 Interactive Mode![/bold]\n")
    console.print(
        "I'll guide you through creating a production-ready feature "
        "for your Next.js + Supabase application.\n"
    )

    # Get feature description
    console.print("[bold cyan]Step 1:[/bold cyan] Describe your feature\n")
    description = Prompt.ask(
        "📝 What feature would you like to build?",
        default="Add a team activity log showing all member actions",
    )

    # Check for existing PRD
    has_prd = Confirm.ask("\n📄 Do you have an existing PRD document?", default=False)

    prd_path = None
    if has_prd:
        prd_input = Prompt.ask("  Enter path to PRD")
        prd_path = Path(prd_input) if prd_input else None

    # Choose workflow mode
    console.print("\n[bold cyan]Step 2:[/bold cyan] Choose workflow mode\n")
    console.print("1. [bold]Full SDLC[/bold] - Complete workflow (PRD → Deployment)")
    console.print("2. [bold]From PRD[/bold] - Skip product phase, use existing PRD")
    console.print("3. [bold]Specific Phase[/bold] - Run only one phase")
    console.print("4. [bold]Specific Agent[/bold] - Run only one agent\n")

    mode_choice = Prompt.ask(
        "Select mode",
        choices=["1", "2", "3", "4"],
        default="1" if not has_prd else "2",
    )

    mode_map = {
        "1": WorkflowMode.FULL,
        "2": WorkflowMode.PRD,
        "3": WorkflowMode.PHASE,
        "4": WorkflowMode.AGENT,
    }
    mode = mode_map[mode_choice]

    # Create feature request
    request = FeatureRequest(
        description=description,
        prd_path=prd_path,
    )

    # Confirm and run
    console.print("\n[bold cyan]Step 3:[/bold cyan] Review and confirm\n")
    console.print(f"  Feature: {description}")
    console.print(f"  Mode: {mode.value}")
    console.print(f"  Target Project: {settings.target_project_path}")
    console.print(f"  Workspace: {settings.workspace_dir}\n")

    if not Confirm.ask("🚀 Ready to start?", default=True):
        console.print("[yellow]Operation cancelled.[/yellow]")
        raise typer.Abort()

    # Run orchestrator
    asyncio.run(run_orchestrator(request, mode))


@app.command()
def full(
    description: str = typer.Argument(..., help="Feature description"),
    prd: Path | None = typer.Option(None, help="Path to existing PRD"),
):
    """
    Run full SDLC workflow (all phases)
    """
    print_banner()

    request = FeatureRequest(
        description=description,
        prd_path=prd,
    )

    asyncio.run(run_orchestrator(request, WorkflowMode.FULL))


@app.command()
def from_prd(
    prd: Path = typer.Argument(..., help="Path to PRD document"),
):
    """
    Start from existing PRD (skip product phase)
    """
    print_banner()

    if not prd.exists():
        console.print(f"[red]Error:[/red] PRD not found: {prd}")
        raise typer.Exit(1)

    # Read PRD to get description
    description = f"Feature from PRD: {prd.name}"

    request = FeatureRequest(
        description=description,
        prd_path=prd,
    )

    asyncio.run(run_orchestrator(request, WorkflowMode.PRD))


@app.command()
def agent(
    agent_name: str = typer.Argument(..., help="Agent role name"),
    task: str = typer.Argument(..., help="Task description"),
    target: Path | None = typer.Option(None, help="Target path (feature package or file)"),
):
    """
    Run a specific agent only
    """
    print_banner()

    request = FeatureRequest(
        description=task,
        metadata={"agent": agent_name, "target": str(target) if target else None},
    )

    asyncio.run(run_orchestrator(request, WorkflowMode.AGENT))


@app.command()
def status(
    execution_id: str | None = typer.Option(None, help="Execution ID to check"),
):
    """
    Check status of a running or completed execution
    """
    console.print("[yellow]Status command not yet implemented[/yellow]")


@app.command()
def list_agents():
    """
    List all available specialist agents
    """
    print_banner()

    console.print("\n[bold]Available Specialist Agents:[/bold]\n")

    phases = {
        "Product Definition": [
            "product-manager",
            "ux-researcher",
            "business-analyst",
        ],
        "Architecture & Design": [
            "solutions-architect",
            "database-architect",
            "security-architect",
        ],
        "Implementation": [
            "database-engineer",
            "backend-engineer",
            "frontend-engineer",
        ],
        "Testing": [
            "qa-engineer",
            "e2e-test-engineer",
            "db-test-engineer",
        ],
        "Security & Review": [
            "security-engineer",
            "code-reviewer",
            "performance-engineer",
        ],
        "Documentation & Deployment": [
            "technical-writer",
            "devops-engineer",
        ],
    }

    for phase, agents in phases.items():
        console.print(f"[bold cyan]{phase}:[/bold cyan]")
        for agent in agents:
            console.print(f"  • {agent}")
        console.print()


@app.command()
def config():
    """
    Show current configuration
    """
    print_banner()

    console.print("\n[bold]Current Configuration:[/bold]\n")

    console.print("[bold cyan]AI Provider:[/bold cyan]")
    console.print(f"  OpenAI: {'✓' if settings.has_openai else '✗'}")
    console.print(f"  Anthropic: {'✓' if settings.has_anthropic else '✗'}")
    console.print(f"  Default Model: {settings.default_agent_model}")

    console.print("\n[bold cyan]Target Project:[/bold cyan]")
    console.print(f"  Path: {settings.target_project_path}")
    console.print(f"  Type: {settings.target_project_type}")

    console.print("\n[bold cyan]Supabase:[/bold cyan]")
    console.print(f"  URL: {settings.supabase_url}")
    console.print(f"  Configured: {'✓' if settings.has_supabase else '✗'}")

    console.print("\n[bold cyan]GitHub:[/bold cyan]")
    console.print(f"  Configured: {'✓' if settings.has_github else '✗'}")
    if settings.has_github:
        console.print(f"  Repo: {settings.github_repo}")

    console.print("\n[bold cyan]Orchestrator:[/bold cyan]")
    console.print(f"  Max Parallel Agents: {settings.max_parallel_agents}")
    console.print(f"  Agent Timeout: {settings.agent_timeout_seconds}s")
    console.print(f"  Workspace Dir: {settings.workspace_dir}")

    console.print("\n[bold cyan]Automation:[/bold cyan]")
    console.print(f"  Auto Commit: {'✓' if settings.enable_auto_commit else '✗'}")
    console.print(f"  Auto PR: {'✓' if settings.enable_auto_pr else '✗'}")
    console.print(f"  Auto Test: {'✓' if settings.enable_auto_test else '✗'}")


async def run_orchestrator(request: FeatureRequest, mode: WorkflowMode):
    """Run the orchestrator"""
    orchestrator = SDLCOrchestrator()

    try:
        execution = await orchestrator.execute_feature_request(request, mode)

        # Print final workspace location
        console.print(
            f"\n[bold green]Workspace:[/bold green] {execution.workspace_context.workspace_path}"
        )

        # Offer to create PR
        if settings.has_github and settings.enable_auto_pr:
            if Confirm.ask("\n🎫 Create GitHub Pull Request?", default=False):
                console.print("[yellow]PR creation not yet implemented[/yellow]")

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
