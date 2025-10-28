import bpy  # type: ignore

# preferences
from .preferences import Sample_Preferences

# Operators
from .operators.CONDUIT_OT_LinkCollection import CONDUIT_OT_LinkCollection
from .operators.CONDUIT_OT_SaveMasterVersion import CONDUIT_OT_SaveMasterVersion
from .operators.CONDUIT_OT_SaveNewVersion import CONDUIT_OT_SaveNewVersion

# panels
from .panels.VIEW3D_PT_UI_Sample import VIEW3D_PT_UI_Sample

# conduit connector (start/stop during register/unregister)
from . import conduit_connector


# reading values such as name, version and more from toml so there is no need to change information in two places
def load_manifest_info():
    from .constants import get_manifest

    manifest = get_manifest()

    # reading addon name
    extension_name = manifest["name"]

    # reading addon version
    version_str = manifest["version"]
    version_tuple = tuple(int(x) for x in version_str.split("."))

    # reading Blender version
    blender_version_str = manifest["blender_version_min"]
    blender_version_tuple = tuple(int(x) for x in blender_version_str.split("."))

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

classes = [
    # preferences
    Sample_Preferences,
    # operators:
    CONDUIT_OT_LinkCollection,
    CONDUIT_OT_SaveMasterVersion,
    CONDUIT_OT_SaveNewVersion,
    # panels:
    VIEW3D_PT_UI_Sample,
]


def register():
    for i in classes:
        bpy.utils.register_class(i)
    # start the conduit connector when the addon is enabled
    try:
        conduit_connector.start_global_connector()
    except Exception:
        # don't fail registration if the connector can't start
        import traceback

        print("Failed to start ConduitConnector:")
        traceback.print_exc()


def unregister():
    # stop connector first to ensure background threads are cleaned up
    try:
        conduit_connector.stop_global_connector()
    except Exception:
        import traceback

        print("Failed to stop ConduitConnector:")
        traceback.print_exc()

    for i in reversed(classes):
        bpy.utils.unregister_class(i)


if __name__ == "__main__":
    register()

