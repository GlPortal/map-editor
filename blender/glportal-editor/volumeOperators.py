import bpy
import os
import string
import re

from .operatorHelpers import *
from .updateTextures import *

class setAcid(bpy.types.Operator):
    bl_idname = "wm.set_acid"
    bl_label = "Acid"
    bl_description = "Mark the selection as a volume of acid."
    bl_options = {"UNDO"}
    
    def execute(self, context):
        mat = getMaterial('textures/fluid/acid00.png', (0.2, 1.0, 0.2))
        bpy.types.Object.glpType = bpy.props.StringProperty()
        object = bpy.context.active_object
        if object:
            if object.type == "MESH":
                if object.glpTypes != "door":
                    resetTriggerSettings(object)
                    
                    object.glpTypes = "volume"
                    object.glpVolumeTypes = "acid"
                    me = object.data
                    if (len(me.materials) == 0):
                        me.materials.append(mat)
                    else:
                        me.materials[0] = mat
                    
                    UpdateTexture.updateTexture(object)
                else:
                    self.report({'ERROR'}, "Door can't be converted to the volume of acid.")
            else:
                self.report({'ERROR'}, "Object of type '%s' can't be converted to the volume of acid." % (object.type))
        return {'FINISHED'}

class addAcid(bpy.types.Operator):
    bl_idname = "wm.add_acid"
    bl_label = "Acid"
    bl_description = "Add a volume of acid."
    bl_options = {"UNDO"}
    
    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add()
        setAcid.execute(self, context)
        return {'FINISHED'}
