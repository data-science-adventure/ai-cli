from rich.console import Console
from rich.status import Status


class MessageUtils:
    """
    A service class to manage Extraction text from different files formats.
    """

    def __init__(self, console: Console):
        self.console = console

    def message(self, icon: str, color: str, message: str):
        self.console.print(f"{color}{icon} {message}")

    def info(self, message: str):
        self.message("🔹", "[blue]", message)

    def success(self, message: str):
        self.message("✅", "[green]", message)

    def error(self, message: str):
        self.message("🔴", "[bold red]", message)

    def warning(self, message: str):
        self.message("⚠️ ", "[bold yellow]", message)

    def status(self, message: str):
        return self.console.status(f"[bold green] {message}")

    def update(self, status: Status, message: str):
        status.update(f"[bold][italic]{message}")
