import os
import sys

def is_docker():
    """Check if the current process is running inside a Docker container."""
    return os.path.exists('/.dockerenv') or os.path.exists('/run/.containerenv')

if __name__ == "__main__":
    # If run on Host (Windows), automatically spawn the external terminal with Docker
    if not is_docker() and os.name == 'nt':
        print("Launching GRNT CODE in external terminal...")
        os.system('start powershell "-NoExit -Command \\"docker-compose build; docker-compose run --rm grnt-code\\""')
        sys.exit(0)

import click
from rich.console import Console
from rich.rule import Rule
from .agent import Agent48

console = Console()

GRNT_LOGO = """
   ▗▟██▙▖
  ▐█[bold cyan]●[/bold cyan]  [bold cyan]●[/bold cyan]█▌   [bold white]GRNT CODE v1.0.0[/bold white]
  ▐▙▄▄▄▄▟▌   [dim]GPU-Ready Resilient Neural Terminal[/dim]
   ▝▜██▛▘    [dim]{model} · {cwd}[/dim]
"""

@click.command()
@click.option('--model', default='granite4:3b', help='Ollama model to use')
def main(model):
    # Initial Launch Sequence
    console.print("\n[bold white]Model Configuration[/bold white]\n")
    console.print(f"Launching [bold cyan]GRNT CODE[/bold cyan] with [bold]{model}[/bold]...")
    
    agent = Agent48(model=model)
    cwd = os.getcwd()
    
    # Header Layout
    console.print(GRNT_LOGO.format(model=model, cwd=cwd))
    console.print(f"[dim]/model to try other local models[/dim]\n")
    console.print(Rule(style="dim"))

    while True:
        try:
            # Main prompt style
            query = click.prompt("❯", prompt_suffix=" ")
            
            if query.lower() in ['exit', 'quit', 'bye']:
                break
            
            if query.lower() == '?':
                console.print("\n[bold cyan]Shortcuts:[/bold cyan]")
                console.print("  [bold]?[/bold]      Show shortcuts")
                console.print("  [bold]exit[/bold]   End session\n")
                continue

            console.print(Rule(style="dim"))
            
            # Response streaming
            for chunk in agent.chat(query):
                console.print(chunk, end="")
            console.print("")
            
            console.print(Rule(style="dim"))
            console.print("  [dim]? for shortcuts[/dim]")
            
        except KeyboardInterrupt:
            console.print("\n[dim]Session terminated.[/dim]")
            break
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()
