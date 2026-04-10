import os
import sys
import click
import subprocess

current_folder = os.path.dirname(__file__)
working_dir = os.path.join(current_folder, '..')
source_folder = os.path.join(working_dir, 'src')
dist_folder = os.path.join(working_dir, 'dist')

sys.path.append(source_folder)

import create_version


@click.command()
@click.option('--cmdline', is_flag=True, help='Cmdline-Mode')
@click.option('--help', '-h', is_flag=True, help='Show this help')
def build(cmdline, help):
    """Build project using PyInstaller"""

    if help:
        click.echo("Usage: python build.py [OPTIONS]")
        click.echo()
        click.echo("Options:")
        click.echo("  --cmdline    Cmdline-Mode")
        click.echo("  --help, -h   Show this help")
        click.echo()
        click.echo("Examples:")
        click.echo("  python build.py              # GUI-Mode")
        click.echo("  python build.py --cmdline    # Cmdline-Mode")
        return

    create_version.main()

    cmd_base = f"python -m PyInstaller --version-file={working_dir}/version_info.rc --distpath {dist_folder} {source_folder}/main.py --clean --onefile --icon={source_folder}/logo.ico --name Kevin"

    if cmdline:
        cmd = f"{cmd_base}_cmdline"
    else:
        cmd = f"{cmd_base} --noconsole"

    subprocess.run(cmd, capture_output=True, text=True)

    os.remove(f"{working_dir}/version_info.rc")

if __name__ == '__main__':
    build()