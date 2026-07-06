"""Launch the DevBrew interactive terminal UI."""

from __future__ import annotations

from devbrew.ui.app import DevBrewApp


def run() -> None:
    """Start the DevBrew Textual app."""
    DevBrewApp().run()


if __name__ == "__main__":
    run()
