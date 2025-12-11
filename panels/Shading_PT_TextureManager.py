import bpy
from ..constants import get_operator, get_preferences
from ..pipeline import get_tasks

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
        self.draw_task_selection_layout(layout)
        self.draw_create_link_box(layout, context=context)
        

    def draw_create_texture_layout(self,layout): 
        create_texture_box = layout.box()
        create_texture_box.scale_y = 1.25
        create_texture_box.label(text = "Create new texture")
        create_texture_row = create_texture_box.row(align=True)
        create_texture_row.prop(self.properties, "TextureSizes", expand=True)

    def draw_task_selection_layout(self,layout):
        task_box = layout.box()
        headline_row = task_box.row()
        headline_row.label(text = "Assign Task")
        headline_row.operator(get_operator("refresh_tasks"), text = "", icon = "FILE_REFRESH")
        task_row = task_box.column()
        task_row.prop(self.properties, "Tasks", expand = True)

    def draw_create_link_box(self, layout, context):

        props = context.scene.TaskProperties


        Files_Box = layout.box()
        Files_Box.template_list(
        "UI_UL_list", 
        "Test", 
        props, "Task_Items", 
        props, "Task_Index")


        create_row = layout.row()
        create_row.scale_y = 1.5

        if len(props.Task_Items) != 0:
            create_row.operator(get_operator("import_texture"), text = "Import")
            create_row.operator(get_operator("create_new_texture"), text = "New Version")



        else:
            create_row.operator(get_operator("create_new_texture"), text = "Create")


