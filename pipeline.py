import bpy #type: ignore
import os
from pathlib import Path

def get_version_from_filename(filename=None, padded = False):
    if filename is None:
        filename = os.path.basename(bpy.data.filepath)  
    if "master" in filename:
        return "master"
    version = int(filename[-9:-6])

    if padded:
        return f"{version:03}"
    return version


def get_expected_filename(self, directory: Path) -> str:
    task = directory
    asset = Path(task).parent
    expected_filename = f"{asset.name}_{task.name}"
    return expected_filename



def get_expected_filename(self, directory: Path) -> str:
    expected_base_filename = get_expected_filename(directory=directory)
    version = get_version_from_filename()
    return str(expected_base_filename + version + ".blend")
