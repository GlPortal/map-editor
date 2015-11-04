import bpy

class setLightCommon(bpy.types.Operator):
    bl_idname = "wm.set_light_common"
    bl_label = "Common"
    bl_description = "Set a light with predefined color for common lights"
    bl_options = {"UNDO"}

    def execute(self, context):
        object = bpy.context.active_object
        if object:
            if object.type == "LAMP":
                lamp = object.data

                lamp.color = [1.0, 0.95, 0.9]
                lamp.use_specular = False
            else:
                self.report({'ERROR'}, "Object of type '%s' can't be converted to the common light." % (object.type))

        return {'FINISHED'}

class addLightCommon(bpy.types.Operator):
    bl_idname = "wm.add_light_common"
    bl_label = "Common"
    bl_description = "Add a light with predefined color for common lights"
    bl_options = {"UNDO"}

    def execute(self, context):
        bpy.ops.object.lamp_add(type = "POINT")
        setLightCommon.execute(self, context)

        return {'FINISHED'}

class setLightEnd(bpy.types.Operator):
    bl_idname = "wm.set_light_end"
    bl_label = "End"
    bl_description = "Set a light with predefined color for end lights"
    bl_options = {"UNDO"}

    def execute(self, context):
        object = bpy.context.active_object
        if object:
            if object.type == "LAMP":
                lamp = object.data

                lamp.color = [0.5, 0.5, 1]
                lamp.distance = 4
                lamp.energy = 5
                lamp.use_specular = False
            else:
                self.report({'ERROR'}, "Object of type '%s' can't be converted to the end light." % (object.type))

        return {'FINISHED'}

class addLightEnd(bpy.types.Operator):
    bl_idname = "wm.add_light_end"
    bl_label = "End"
    bl_description = "Add a light with predefined color for end lights"
    bl_options = {"UNDO"}

    def execute(self, context):
        bpy.ops.object.lamp_add(type = "POINT")
        setLightEnd.execute(self, context)

        return {'FINISHED'}
