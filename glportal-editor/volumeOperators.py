import bpy

from .operatorHelpers import resetTriggerSettings

class setAcid(bpy.types.Operator):
  bl_idname = "glp.set_acid"
  bl_label = "Acid"
  bl_description = "Mark the selection as a volume of acid."
  bl_options = {'UNDO'}

  def execute(self, context):
    object = bpy.context.active_object
    if object:
      if object.type == 'MESH':
        if object.glpTypes != "door":
          if object.glpTypes != "model":
            resetTriggerSettings(object)

            object.glpTypes = "volume"
            object.glpVolumeTypes = "acid"

          object.glpMaterial = "fluid/acid00"
        else:
          self.report({'ERROR'}, "Door can't be converted to the volume of acid.")
      else:
        self.report({'ERROR'}, "Object of type '%s' can't be converted to the volume of acid." % (object.type))
    return {'FINISHED'}

class addAcid(bpy.types.Operator):
  bl_idname = "glp.add_acid"
  bl_label = "Acid"
  bl_description = "Add a volume of acid."
  bl_options = {'UNDO'}

  def execute(self, context):
    bpy.ops.mesh.primitive_cube_add()
    bpy.ops.glp.set_acid()
    return {'FINISHED'}
