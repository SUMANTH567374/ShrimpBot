from llm_synthesis import generate_answer  # Only this is needed now
from rich.console import Console
import time
import os

console = Console()

def clear_screen():
    """Clears the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")

def main():
    console.print("\n🤠 [bold cyan]Welcome to ShrimpBot![/bold cyan] Ask me hatchery SOP questions.\nType [yellow]'exit'[/yellow] to quit or [green]'help'[/green] to see available commands.\n")

    while True:
        try:
            query = input("You: ").strip()

            if not query:
                console.print("[bold red]Please enter a question.[/bold red]")
                continue

            if query.lower() in ["exit", "quit"]:
                console.print("\nShrimpBot: [bold green]Bye! Stay safe at the hatchery 🐟[/bold green]")
                break

            if query.lower() == "help":
                console.print("""
[bold green]Available Commands:[/bold green]
• [yellow]exit[/yellow] - Quit the chatbot
• [yellow]help[/yellow] - Show this message
• [yellow]clear[/yellow] - Clear the screen
""")
                continue

            if query.lower() == "clear":
                clear_screen()
                continue

            start_time = time.time()

            # Use the external function
            response = generate_answer(query)

            elapsed = round(time.time() - start_time, 2)
            console.print(f"[bold blue]ShrimpBot:[/bold blue] {response} [dim](answered in {elapsed}s)[/dim]\n")

        except KeyboardInterrupt:
            console.print("\n[bold red]Interrupted. Exiting...[/bold red]")
            break

        except Exception as e:
            console.print(f"[bold red]⚠️ Error:[/bold red] {e}\n")

if __name__ == "__main__":
    main()
