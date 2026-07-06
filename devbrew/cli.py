"""DevBrew command-line entry point.

For now this exposes a minimal Typer app so the `devbrew` command and packaging
are valid. Interactive TUI screens and the full command set (menu, track,
history, health) arrive with their corresponding Jira stories.
"""

from __future__ import annotations

import typer

from devbrew import __version__

app = typer.Typer(help="DevBrew - order coffee from your terminal.")


@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(
        False, "--version", "-v", help="Show the DevBrew version and exit."
    ),
) -> None:
    """DevBrew - order coffee from your terminal."""
    if version:
        typer.echo(f"DevBrew {__version__}")
        raise typer.Exit()


if __name__ == "__main__":
    app()
