import bpy
import os

from .operatorHelpers import resetTriggerSettings, itemsMaterial
from .managers import MaterialManager, ModelManager

# we are using this for <end> (exit door)
class addDoor(bpy.types.Operator):
  bl_idname = "glp.add_door"
  bl_label = "Add a door"
  #bl_description = "Add a door." # for the future
  bl_description = "Add an exit door (use only once)"
  bl_options = {'UNDO'}

  def execute(self, context):
    prefs = context.user_preferences.addons[__package__].preferences

    ModelManager.create("Door", "door/door")

    object = bpy.context.selected_objects[0]
    if object:
      object.glpTypes = "door"

    return {'FINISHED'}

class setPortalable(bpy.types.Operator):
  bl_idname = "glp.set_portalable"
  bl_label = "Portalable"
  bl_description = "Mark the selection as portalable wall."
  bl_options = {'UNDO'}

  def execute(self, context):
    object = bpy.context.active_object
    if object:
      if object.type == 'MESH':
        if object.glpTypes != "door":
          resetTriggerSettings(object)

          object.glpTypes = "wall"
          object.glpMaterial = "concrete/wall00"
        else:
          self.report({'ERROR'}, "Door can't be converted to the portalable wall.")
      else:
        self.report({'ERROR'}, "Object of type '%s' can't be converted to the portalable wall." % (object.type))
    return {'FINISHED'}

class setWall(bpy.types.Operator):
  bl_idname = "glp.set_wall"
  bl_label = "Metal tiles"
  bl_description = "Mark the selection as metal wall."
  bl_options = {'UNDO'}

  def execute(self, context):
    object = bpy.context.active_object
    if object:
      if object.type == 'MESH':
        if object.glpTypes != "door":
          resetTriggerSettings(object)

          object.glpTypes = "wall"
          object.glpMaterial = "metal/tiles00x3"
        else:
          self.report({'ERROR'}, "Door can't be converted to the metal wall.")
      else:
        self.report({'ERROR'}, "Object of type '%s' can't be converted to the metal wall." % (object.type))
    return {'FINISHED'}

class addWall(bpy.types.Operator):
  bl_idname = "glp.add_wall"
  bl_label = "Metal tiles"
  bl_description = "Add a metal wall."
  bl_options = {'UNDO'}

  def execute(self, context):
    bpy.ops.mesh.primitive_cube_add()
    bpy.ops.glp.set_wall()
    return {'FINISHED'}

class addPortalable(bpy.types.Operator):
  bl_idname = "glp.add_portalable"
  bl_label = "Portalable"
  bl_description = "Add a portalable wall."
  bl_options = {'UNDO'}

  def execute(self, context):
    bpy.ops.mesh.primitive_cube_add()
    bpy.ops.glp.set_portalable()
    return {'FINISHED'}

class searchMaterial(bpy.types.Operator):
  bl_idname = "glp.search_material"
  bl_label = "Set material"
  bl_property = "materials"

  materials = bpy.props.EnumProperty(items=itemsMaterial)

  def execute(self, context):
    object = bpy.context.active_object
    if object and object.type == 'MESH' and object.glpTypes:
      object.glpMaterial = self.materials
    return {'FINISHED'}

  def invoke(self, context, event):
    wm = context.window_manager
    wm.invoke_search_popup(self)
    return {'FINISHED'}
