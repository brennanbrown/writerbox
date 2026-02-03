"""Command-line interface for WriterBox."""

import click
from pathlib import Path
import sys

from .ui import run_ui


@click.command()
@click.option(
    "--dir", "-d",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=Path.cwd(),
    help="Directory to scan for markdown files",
)
@click.option(
    "--recursive", "-r",
    is_flag=True,
    default=True,
    help="Scan subdirectories recursively",
)
@click.option(
    "--no-recursive",
    is_flag=True,
    help="Disable recursive scanning",
)
@click.option(
    "--editor", "-e",
    help="Text editor to use for opening files",
)
@click.option(
    "--config",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Path to configuration file",
)
@click.option(
    "--no-config",
    is_flag=True,
    help="Ignore configuration file",
)
@click.option(
    "--sort",
    type=click.Choice(["date", "date_desc", "date_asc", "title", "word_count"]),
    default="date_desc",
    help="Sort method for files",
)
@click.version_option(
    version="0.1.0-alpha",
    message="WriterBox v%(version)s - A terminal-based writing collection manager\nCreated by Brennan Brown (https://brennan.day)"
)
def main(dir, recursive, no_recursive, editor, config, no_config, sort):
    """WriterBox - A beautiful terminal-based writing collection manager.
    
    Organize and browse your markdown files with style.
    
    Repository: https://github.com/brennanbrown/writerbox
    """
    # Handle recursive flag logic
    if no_recursive:
        recursive = False
    
    try:
        run_ui(dir, recursive, sort)
    except KeyboardInterrupt:
        click.echo("\nThanks for using WriterBox! 📝")
        sys.exit(0)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        click.echo("If this persists, please report it at: https://github.com/brennanbrown/writerbox/issues")
        sys.exit(1)


if __name__ == "__main__":
    main()
