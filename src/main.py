import click
from rich.console import Console
from rich.panel import Panel
from .agent import Agent48

console = Console()

GRNT_ART = """
   ______ ____   _   __ ______
  / ____// __ \ / | / //_  __/
 / / __ / /_/ //  |/ /  / /   
/ /_/ // _, _// /|  /  / /    
\____//_/ |_|/_/ |_/  /_/     
   ______ ____   ____   ______
  / ____// __ \ / __ \ / ____/
 / /    / / / // / / // __/   
/ /___ / /_/ // /_/ // /___   
\____/ \____//_____//_____/   
"""

@click.command()
@click.option('--model', default='granite4:3b', help='Ollama model to use')
def main(model):
    console.print(Panel(f"[bold cyan]{GRNT_ART}[/bold cyan]\n[bold white]GRNT CODE CLI[/bold white]\n[dim]Functional • Direct • Local[/dim]", expand=False))
    console.print(f"Model: [cyan]{model}[/cyan]")
    
    agent = Agent48(model=model)
    
    while True:
        try:
            query = click.prompt("\n[bold cyan]PROMPT[/bold cyan] >")
            if query.lower() in ['exit', 'quit', 'bye']:
                break
            
            console.print("\n[bold green]Response:[/bold green]")
            for chunk in agent.chat(query):
                console.print(chunk, end="")
            console.print("\n")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()
