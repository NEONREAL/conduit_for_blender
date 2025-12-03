import bpy  # type: ignore
from .constants import get_operator


class Sample_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    username: bpy.props.StringProperty(
        name="Username", default="Fxnarji", description="Enter your username"
    )  # type: ignore

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        # Pass `self` as the owner of the property
        box.prop(self, "username")
        box.operator(get_operator("register_blender"), text="Register Blender Executable")
