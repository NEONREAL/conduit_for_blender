import bpy #type: ignore
from pathlib import Path
import re
import json
import os
from .ConduitClient import send_command
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

def is_conduit_file() -> bool:
    filepath = Path(bpy.data.filepath)
    if not filepath:
        return False
    
    asset_path = filepath.parent.parent
    for file in asset_path.iterdir():
        if file.suffix == ".sidecar":
            return True
    print(asset_path)
    return False

def get_task_name() -> str | None:
    filepath = Path(bpy.data.filepath)
    if not filepath:
        return None
    task_name = filepath.parent.name
    return task_name

def get_task_info() -> dict | None:
    asset = Path(bpy.data.filepath).parent.parent
    task = Path(bpy.data.filepath).parent
    rel_task_path = os.path.join(asset, task)
    unity_path = send_command("get_setting",entry="unity_path")
    if not unity_path:
        return None
    if unity_path["status"] != "ok":
        return None
    unity_path = unity_path["entry_value"]
    unity_path = os.path.join(unity_path, rel_task_path)
    task_info = {
        "asset_name": asset.name,
        "task_name": task.name,
        "unity_path": unity_path
    }
    return task_info
