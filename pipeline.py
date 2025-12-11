import bpy #type: ignore
from pathlib import Path
import re
import json
import os
from .ConduitClient import send_command
from .constants import get_preferences
from pathlib import Path

def get_version_from_filename(filename: str, padded = False, next_version: bool = True) -> str | None:
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

def get_expected_filename(directory: Path) -> tuple[str, str]:
    task = directory.parent
    asset = Path(task).parent
    expected_filename = f"{asset.name}_{task.name}"
    return expected_filename, asset.name

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

def get_latest_version(task: Path | dict, next_version = False) -> tuple[str, str | None] | None:
    if isinstance(task, dict):
        task_path = task.get("path")
        if not task_path:
            return None
    elif isinstance(task, Path):
        task_path = task
    else:
        return None
    
    res = send_command("get_setting", entry = "ignored_suffix")
    if not res or res["status"] != "ok":
        ignored_files = [".blend1", ".tmp", ".json"]
    else:
        ignored_files = res["entry_value"]

    latest_version = -1
    latest_file: str = None

    for file in task_path.iterdir():
        if file.suffix in ignored_files:
            continue
        version = int(get_version_from_filename(file.name, padded=False, next_version=next_version))

        if not version:
            return "001", None
        print(type(version))
        print(type(latest_version))

        if version is not None and version > latest_version:
            latest_version = version
            latest_file = file
        
    latest_version = f"{latest_version:03}"
    if next_version:
        filename = str(latest_file)
        suffix = filename.split('.')[-1]
        stem = filename.split('.')[0]
        print(stem)
        stem_no_version = stem[:-4]
        latest_file = f"{stem_no_version}_{latest_version}.{suffix}"

    Path(latest_file).touch(exist_ok=True)
    print(f"touched {latest_file}")
    return latest_version, latest_file

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
    rel_task_path = os.path.join(asset.name, task.name)
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

def get_Asset_info() -> dict | None:
    asset = Path(bpy.data.filepath).parent.parent
    result = send_command("get_asset_info", path = str(asset))
    if not result:
        return
    if "ok" in result["status"]:
        Asset_info = result["asset"]
    return Asset_info

def get_tasks() -> list:
    info = get_Asset_info()
    print(f"info: {info}")
    if not info:
        return []
    if "tasks" in info:
        print(info["tasks"])
        return info["tasks"]
    return []

def update_task_list(context) -> None:
    res = send_command("get_setting", entry = "ignored_suffix")
    if not res or res["status"] != "ok":
        ignored_files = [".blend1", ".tmp", ".json"]
    else:
        ignored_files = res["entry_value"]

    props = context.scene.conduit_texture_properties

    props.task_items.clear()
    tasks = get_tasks()
    for task in tasks:
        if task.get('type') != 'texture':
            continue
        item = props.task_items.add()
        item.name = task.get('name')
        item.path = task.get('path')



    props = context.scene.TaskProperties
    props.Task_Items.clear()
    selected_task = Path(context.scene.conduit_texture_properties.Tasks)
    for files in selected_task.iterdir():
        if files.suffix.lower() in ignored_files:
            continue
        item = props.Task_Items.add()
        item.name = files.stem
        item.path = str(files)
        item.version = str(get_version_from_filename(files.name, padded=True, next_version=False))
    
def add_texture_to_shader(image, material) -> None:
    name = image.name
    nodes = material.node_tree.nodes
    # putting into shader
    if name in nodes:
        texture_node = nodes[name]
    else:
        texture_node = nodes.new(type='ShaderNodeTexImage')
    texture_node.image = image
    texture_node.name = name
    texture_node.label = Path(image.filepath).name