import sys
import os
import subprocess

current_folder = os.path.dirname(__file__)

sys.path.append(os.path.join(current_folder, '../src'))

from config_params import glob_cfg_version_string
from PyInstaller.utils.win32 import versioninfo


def get_git_info():
    try:
        working_dir = os.path.join(current_folder, '..')
        os.chdir(working_dir)

        # Commit-Hash (erste 6 Zeichen)
        commit_hash = subprocess.run(
            ['git', 'rev-parse', '--short=6', 'HEAD'],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        # Dirty-Status prüfen
        dirty_status = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            check=True
        )

        is_dirty = bool(dirty_status.stdout.strip())

        return commit_hash, is_dirty
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None, False


def main():
    commit_hash, is_dirty = get_git_info()

    # Basis-Version
    version_string = glob_cfg_version_string

    if commit_hash:
        version_string = f"{version_string}_{commit_hash[:6]}"
        if is_dirty:
            version_string = f"{version_string}_dirty"
            print(f"Git-Repository is dirty!")
        print(f"Git-Commit: {commit_hash[:6]}")

    print(f"Using Version: {version_string}")

    version_tuple = tuple(map(int, glob_cfg_version_string.split('.'))) + (0,)

    vs_info = versioninfo.VSVersionInfo(
        ffi=versioninfo.FixedFileInfo(
            filevers=version_tuple,
            prodvers=version_tuple,
            mask=0x3f,
            flags=0x0,
            OS=0x40004,
            fileType=0x1,
            subtype=0x0,
            date=(0, 0)
        ),
        kids=[
            versioninfo.StringFileInfo(
                [versioninfo.StringTable('040904B0',
                                         [versioninfo.StringStruct('ProductVersion', version_string)])]
            ),
            versioninfo.VarFileInfo([versioninfo.VarStruct('Translation', [0x409, 1200])])
        ]
    )

    file_path = os.path.join(current_folder, '../version_info.rc')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(vs_info))

    print(f"Version info created: {version_string}")


if __name__ == "__main__":
    main()