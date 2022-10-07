from pathlib import Path
import string
from typing import List
import bpy
from bpy import context, types, app, ops, props
from bpy.app.handlers import persistent
import os

from bpy.utils import register_class, unregister_class


@persistent
def capture(index: string):
    ops.render.opengl(sequencer=True)
    rndr_img = bpy.data.images["Render Result"]
    name = "anotation"+index+".png"
    path = app.tempdir+name
    rndr_img.save_render(filepath=path)
    ops.image.open(filepath=path)
    bpy.data.images[name].pack()

bpy.app.handlers.save_post.append(capture)

class ListItem(types.PropertyGroup):
    name: props.StringProperty(
        name="Name", description="A name for this item", default="Untitled")
    frame: props.IntProperty(
        name="Frame", description="", default=0)


class ARIG_OT_setup_anotation(types.Operator):
    bl_idname = "avid.setup_annotation"
    bl_label = "setup_annotation"

    def execute(self, context: context):
        print("start viewport render")

        items = context.scene.annotations
        item = items.add()
        item.name = "annotation "+str((len(items)))
        item.frame = context.scene.frame_current
        print(len(items))
        capture(str(len(items)))
        path = Path(__file__).parent
        lib_name = 'lib.blend'
        lib_filename = "annotation-template"
        lib_path = os.path.join(path, lib_name)
        lib_directory = os.path.join(lib_path, "Scene")
        lib_filepath = os.path.join(lib_directory, lib_filename)
        ops.wm.append(filepath=lib_filepath,
                      directory=lib_directory, filename=lib_filename)
        scene = bpy.data.scenes['annotation-template']
        scene.name = item.name
        cam = bpy.data.cameras[scene.camera.data.name]
        cam.show_background_images = True
        bg = cam.background_images.new()
        bg.image = bpy.data.images["anotation"+str((len(items)))+".png"]

        return {'FINISHED'}


class ARIG_OT_delete(types.Operator):
    bl_idname = "avid.delete"
    bl_label = "test"

    def execute(self, context: context):
        index = context.scene.annotation_index
        context.scene.annotations.remove(index)
        return {'FINISHED'}


class ARIG_OT_resnap(types.Operator):
    bl_idname = "avid.resnap"
    bl_label = "Re Snap the frame information"

    def execute(self, context: context):
        index = context.scene.annotation_index
        print(context.scene.annotation_index)
        capture(str(index+1))
        context.scene.annotations[index].frame = context.scene.frame_current
        return {'FINISHED'}


class ARIG_OT_edit(types.Operator):
    bl_idname = "avid.edit"
    bl_label = "Edit Anotation"

    def execute(self, context: context):
        print(context.scene.annotation_index)
        index = context.scene.annotation_index
        annotation = context.scene.annotations[index]
        # import
        path = Path(__file__).parent
        lib_name = 'lib.blend'
        lib_path = os.path.join(path, lib_name)
        lib_workspacename = "Annotation Editor"
        if not lib_workspacename in bpy.data.workspaces:
            ops.workspace.append_activate(
                idname=lib_workspacename, filepath=lib_path)

        context.window.workspace = bpy.data.workspaces['Annotation Editor']
        # context.window.scene = data.scenes[annotation.name]

        return {'FINISHED'}

classes = (
    ARIG_OT_setup_anotation,
    ARIG_OT_delete,
    ARIG_OT_edit,
    ARIG_OT_resnap,
    ListItem
)


def register():
    for c in classes:
        register_class(c)
    types.Scene.annotations = props.CollectionProperty(type=ListItem)
    types.Scene.annotation_index = props.IntProperty(
        name="annotation_index", default=0)


def unregister():
    for c in classes:
        unregister_class(c)
