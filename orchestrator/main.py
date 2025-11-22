"""
TAC-9 Orchestrator - Main Entry Point
"""

from rich.console import Console

from orchestrator.cli import app

console = Console()


def main():
    """Main entry point"""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"\n[bold red]Fatal error:[/bold red] {e}")
        raise


if __name__ == "__main__":
    main()
