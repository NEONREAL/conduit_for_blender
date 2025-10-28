import bpy #type: ignore
import os
from pathlib import Path
import re
import json
from .constants import get_preferences

def get_version_from_filename(filename: str, padded = False, next_version: bool = True) -> int | str | None:
    pattern = re.compile(r"^(.*?)(\d+)\.([a-zA-Z0-9]+)$") #matches: any string + any int + file extension

    match = pattern.match(filename)
    if not match:
        return None

    version = int(match.group(2))

    if next_version:
        version += 1

    if padded:
        return f"{version:03}"
    return version


def get_expected_filename(directory: Path) -> str:
    task = directory.parent
    asset = Path(task).parent
    expected_filename = f"{asset.name}_{task.name}"
    print(f"asset name: {asset.name}, task name: {task.name}")
    print(f"expected filename: {expected_filename}")
    return expected_filename

def create_json_info(comment: str | None = None) -> None:
    comment = comment or "test"
    filepath = Path(bpy.data.filepath)
    filename = filepath.stem 
    json_path = filepath.parent / f"{filename}.versioninfo"
    username = get_preferences().username
    print(f"username is: {username}")
    data = {
        "user": username,
        "comment": comment
    }
    
    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)