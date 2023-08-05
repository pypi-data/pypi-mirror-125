# -*- coding: utf-8 -*-
"""Command-line interface and logging configuration."""
# standard-library imports

from typing import Optional

import typer

from . import VERSION
from .common import APP
from .common import STATE
from .plddt import plddt_truncate

# global constants
unused_commands = (plddt_truncate,)
click_object = typer.main.get_command(APP)  # noqa: F841

def version_callback(value: bool) -> None:
    """Print version info."""
    if value:
        typer.echo(f"{APP.info.name} version {VERSION}")
        raise typer.Exit()


VERSION_OPTION = typer.Option(
    None,
    "--version",
    callback=version_callback,
    help="Print version string.",
)


@APP.callback()
def set_global_state(
    verbose: bool = False,
    quiet: bool = False,
    version: Optional[bool] = VERSION_OPTION,
) -> None:
    """Set global-state variables."""
    if verbose:
        STATE["verbose"] = True
        STATE["log_level"] = "DEBUG"
    elif quiet:
        STATE["log_level"] = "ERROR"
    unused_state_str = f"{version}"  # noqa: F841


def main() -> None:
    """Run the app."""
    APP()
