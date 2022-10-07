# context.area: SEQUENCE_EDITOR

from bpy import types, context, utils
from bpy.utils import register_class, unregister_class


class UI_PT_AV_List(types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.label(text=item.name)
        layout.label(text=str(item.frame))

    def invoke(self, context, event):
        pass


class UI_PT_AV_Avid(types.Panel):
    bl_idname = "UI_PT_AV_Avid"
    bl_label = "Tools"
    bl_category = "avid"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context: context):
        layout = self.layout
        row = layout.row(align=True)
        row.operator("avid.setup_annotation", text="Setup Annotation")
        row.operator("avid.delete", text="Delete")
        row = layout.row(align=True)
        # row.enabled = False
        if 'annotations' in context.scene:
            row.template_list("UI_PT_AV_List", "", context.scene,
                              "annotations", context.scene, "annotation_index")
            row = layout.row(align=True)
            row.operator("avid.resnap", icon="RESTRICT_RENDER_OFF",
                        text="Re Shoot")
            row.operator("avid.edit", icon="GREASEPENCIL", text="Edit Anotation")


classes = (
    UI_PT_AV_List,
    UI_PT_AV_Avid
)


def register():
    for c in classes:
        register_class(c)


def unregister():
    for c in classes:
        unregister_class(c)
