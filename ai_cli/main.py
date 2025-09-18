import sys
import typer
import platform
from rich.console import Console

# Import sub-command applications from other modules.
from .commands.inference_commands import inference_app

# Initialize the main Typer application with a help message.
app = typer.Typer(help="A CLI for managing NLP tasks")

# Add the sub-command applications to the main app. This creates a nested
# command structure (e.g., `cli extract`, `cli model`, `cli dataset`).
app.add_typer(inference_app, name="inference")

# Get a rich console instance and a default context object.
# These will be used by the commands to provide formatted output and
# access to shared configuration.
console = Console()


@app.command(help="Show the messages")
def messages():
    """
    Demonstrates the various message types available via MessageUtils.
    """
    from ai_cli.utils.message_utils import MessageUtils

    message_util = MessageUtils(console)
    # Print different types of messages to the console with appropriate styling.
    message_util.info("This is a information message")
    message_util.warning("This is a warning message")
    message_util.error("This is an error message")
    message_util.success("This is a success message")


# This standard Python construct ensures the application only runs
# when the script is executed directly.
if __name__ == "__main__":
    app()
