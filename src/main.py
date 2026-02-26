import os
import sys
import platform

def is_docker():
    """Check if the current process is running inside a Docker container."""
    return os.path.exists('/.dockerenv') or os.path.exists('/run/.containerenv')

def spawn_external_terminal(command):
    """Spawns a new terminal window based on the OS with multi-terminal support."""
    cwd = os.getcwd()
    
    # Check for docker compose vs docker-compose
    docker_check = "docker compose version > /dev/null 2>&1" if os.name != 'nt' else "docker compose version > nul 2>&1"
    if os.system(docker_check) == 0:
        command = command.replace("docker-compose", "docker compose")

    if os.name == 'nt':
        # Windows: Use start with a title to avoid quote parsing issues
        # -NoExit keeps the window open. & { ... } is the PS command block.
        os.system(f'start "GRNT CODE" powershell -NoExit -Command "& {{ {command} }}"')
    elif sys.platform == 'darwin':
        # macOS: Try iTerm2 first, then system Terminal
        iterm_check = "osascript -e 'id of application \"iTerm\"' > /dev/null 2>&1"
        if os.system(iterm_check) == 0:
            iterm_script = f'tell application "iTerm" to create window with default profile command "bash -c \\"cd {cwd} && {command}; exec bash\\""'
            os.system(f"osascript -e '{iterm_script}'")
        else:
            terminal_script = f'tell application "Terminal" to do script "cd {cwd} && {command}"'
            os.system(f"osascript -e '{terminal_script}'")
    else:
        # Linux: Try standard x-terminal-emulator first
        if os.system("which x-terminal-emulator > /dev/null 2>&1") == 0:
            os.system(f"x-terminal-emulator -e \"bash -c '{command}; exec bash'\"")
            return
            
        # Try common terminals
        terminals = ['gnome-terminal', 'konsole', 'xfce4-terminal', 'xterm', 'terminator']
        for term in terminals:
            if os.system(f"which {term} > /dev/null 2>&1") == 0:
                if term == 'gnome-terminal':
                    os.system(f"{term} -- bash -c \"{command}; exec bash\"")
                else:
                    os.system(f"{term} -e \"bash -c '{command}; exec bash'\"")
                return
        # Fallback
        print(f"No external terminal found. Running mission in current session...")
        os.system(command)

if __name__ == "__main__":
    if not is_docker():
        print("\n\033[1;36mLaunching GRNT CODE in external terminal...\033[0m")
        docker_cmd = "docker-compose build; docker-compose run --rm grnt-code"
        spawn_external_terminal(docker_cmd)
        sys.exit(0)

    # Everything below only runs INSIDE Docker
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
    def main_entry(model):
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

    main_entry()
