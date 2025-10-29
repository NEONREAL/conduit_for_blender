import bpy  # type: ignore
import json
from . import BlenderServer

# Preferences
from .preferences import Sample_Preferences

# Operators
from .operators.CONDUIT_OT_LinkCollection import CONDUIT_OT_LinkCollection
from .operators.CONDUIT_OT_SaveMasterVersion import CONDUIT_OT_SaveMasterVersion
from .operators.CONDUIT_OT_SaveNewVersion import CONDUIT_OT_SaveNewVersion

# Panels
from .panels.VIEW3D_PT_UI_AssetManager import VIEW3D_PT_UI_AssetManager
from .panels.VIEW3D_PT_UI_ServerStatus import VIEW3D_PT_UI_ServerStatus

# Module-level variable for the server instance
_server_instance: BlenderServer.BlenderServer | None = None

# Read addon manifest info
def load_manifest_info():
    from .constants import get_manifest

    manifest = get_manifest()

    extension_name = manifest["name"]
    version_tuple = tuple(int(x) for x in manifest["version"].split("."))
    blender_version_tuple = tuple(int(x) for x in manifest["blender_version_min"].split("."))

    bl_info = {
        "name": extension_name,
        "version": version_tuple,
        "blender": blender_version_tuple,
    }
    return bl_info

blender_manifest = load_manifest_info()
bl_info = {
    "name": blender_manifest["name"],
    "description": "Adds RIG UI for Supported Rigs",
    "author": "Your Name",
    "version": blender_manifest["version"],
    "blender": blender_manifest["blender"],
    "location": "Npanel",
    "support": "COMMUNITY",
    "category": "UI",
}

# Classes to register
classes = [
    Sample_Preferences,
    CONDUIT_OT_LinkCollection,
    CONDUIT_OT_SaveMasterVersion,
    CONDUIT_OT_SaveNewVersion,
    VIEW3D_PT_UI_ServerStatus,
    VIEW3D_PT_UI_AssetManager,
]

def register():
    global _server_instance

    for cls in classes:
        bpy.utils.register_class(cls)

    # Create and start the server
    _server_instance = BlenderServer.BlenderServer()
    _server_instance.start(background=True)  # runs in background thread

def unregister():
    global _server_instance

    # Stop server if running
    if _server_instance:
        _server_instance.stop()
        _server_instance = None

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
