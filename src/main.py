import os
import sys

def is_docker():
    """Check if the current process is running inside a Docker container."""
    return os.path.exists('/.dockerenv') or os.path.exists('/run/.containerenv')

def spawn_external_terminal(command):
    """Spawns a new terminal window based on the OS."""
    if os.name == 'nt':
        # Windows
        os.system(f'start powershell "-NoExit -Command \\"{command}\\""')
    elif sys.platform == 'darwin':
        # macOS
        os.system(f"osascript -e 'tell application \"Terminal\" to do script \"cd {os.getcwd()} && {command}\"'")
    else:
        # Linux - try common terminals
        terminals = ['gnome-terminal', 'konsole', 'xfce4-terminal', 'xterm', 'terminator']
        for term in terminals:
            if os.system(f"which {term} > /dev/null 2>&1") == 0:
                if term == 'gnome-terminal':
                    os.system(f"{term} -- bash -c \"{command}; exec bash\"")
                else:
                    os.system(f"{term} -e \"bash -c '{command}; exec bash'\"")
                return
        # Fallback: just run in current session if no GUI terminal is found
        print(f"No external terminal found. Running mission in current session...")
        os.system(command)

if __name__ == "__main__":
    # If run on Host (Any OS), automatically spawn the external terminal with Docker
    if not is_docker():
        print(f"Launching [bold cyan]GRNT CODE[/bold cyan] in external terminal...")
        docker_cmd = "docker-compose build; docker-compose run --rm grnt-code"
        spawn_external_terminal(docker_cmd)
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
