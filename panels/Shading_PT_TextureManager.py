import bpy
from ..constants import get_operator, get_preferences

class Shading_PT_TextureManager(bpy.types.Panel):
    bl_label = "Conduit Texture"
    bl_idname = "PT_Export_Texture"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Conduit"

    def draw(self, context):
        self.properties = context.scene.conduit_texture_properties


        layout = self.layout
        self.draw_create_texture_layout(layout)

    def draw_create_texture_layout(self,layout): 
        create_texture_box = layout.box()
        create_texture_box.scale_y = 1.25
        
        create_texture_box.label(text = "Create new texture")
        create_texture_row = create_texture_box.row(align=True)
        create_texture_row.prop(self.properties, "TextureSizes", expand=True)
        create_texture_box.operator(get_operator("create_new_texture"))

