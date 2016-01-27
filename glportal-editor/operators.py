import bpy
import os

from .operatorHelpers import *
from .managers import MaterialManager

# we are using this for <end> (exit door)
class addDoor(bpy.types.Operator):
  bl_idname = "wm.add_door"
  bl_label = "Add a door"
  #bl_description = "Add a door." # for the future
  bl_description = "Add an exit door (use only once)"
  bl_options = {"UNDO"}

  def execute(self, context):
    prefs = context.user_preferences.addons[__package__].preferences

    realpath = os.path.expanduser(prefs.dataDir + "meshes/Door.obj")
    bpy.ops.import_scene.obj(filepath = realpath)
    bpy.types.Object.glpType = bpy.props.StringProperty()

    mat = MaterialManager.create('door/door', (1, 1, 1))
    mat.texture_slots[0].texture_coords = 'UV'
    mat.texture_slots[0].mapping = 'FLAT'

    obj_objects = bpy.context.selected_objects[:]

    for object in obj_objects:
      if object.glpTypes and object.glpTypes == "none":
        object.location = context.scene.cursor_location
        object.glpTypes = "door"
        context.scene.objects.active = object
        bpy.ops.object.transform_apply(rotation=True)

        me = object.data
        if (len(me.materials) == 0):
          me.materials.append(mat)
        else:
          me.materials[0] = mat

        fixDoorTexture(me)

    return {'FINISHED'}

class setPortalable(bpy.types.Operator):
  bl_idname = "wm.set_portalable"
  bl_label = "Portalable"
  bl_description = "Mark the selection as portalable wall."
  bl_options = {"UNDO"}

  def execute(self, context):
    bpy.types.Object.glpType = bpy.props.StringProperty()
    object = bpy.context.active_object
    if object:
      if object.type == "MESH":
        if object.glpTypes != "door":
          resetTriggerSettings(object)

          object.glpTypes = "wall"
          object.glpWallTypes = "portalable"

          MaterialManager.set(object, "concrete/wall00", (1, 1, 1))
        else:
            self.report({'ERROR'}, "Door can't be converted to the portalable wall.")
      else:
        self.report({'ERROR'}, "Object of type '%s' can't be converted to the portalable wall." % (object.type))
    return {'FINISHED'}

class setWall(bpy.types.Operator):
  bl_idname = "wm.set_wall"
  bl_label = "Metal tiles"
  bl_description = "Mark the selection as metal wall."
  bl_options = {"UNDO"}

  def execute(self, context):
    bpy.types.Object.glpType = bpy.props.StringProperty()
    object = bpy.context.active_object
    if object:
      if object.type == "MESH":
        if object.glpTypes != "door":
          resetTriggerSettings(object)

          object.glpTypes = "wall"
          object.glpWallTypes = "default"

          MaterialManager.set(object, "metal/tiles00x3", (0.2, 0.2, 0.2))
        else:
          self.report({'ERROR'}, "Door can't be converted to the metal wall.")
      else:
        self.report({'ERROR'}, "Object of type '%s' can't be converted to the metal wall." % (object.type))
    return {'FINISHED'}

class addWall(bpy.types.Operator):
  bl_idname = "wm.add_wall"
  bl_label = "Metal tiles"
  bl_description = "Add a metal wall."
  bl_options = {"UNDO"}

  def execute(self, context):
    bpy.ops.mesh.primitive_cube_add()
    setWall.execute(self, context)
    return {'FINISHED'}

class addPortalable(bpy.types.Operator):
  bl_idname = "wm.add_portalable"
  bl_label = "Portalable"
  bl_description = "Add a portalable wall."
  bl_options = {"UNDO"}

  def execute(self, context):
    bpy.ops.mesh.primitive_cube_add()
    setPortalable.execute(self, context)
    return {'FINISHED'}
