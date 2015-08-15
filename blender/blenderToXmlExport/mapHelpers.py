import bpy
from bpy.props import *

def countObjects(context):
    objects = context.scene.objects
    result = {
        'camera':           0,
        'wallPortalable':   0,
        'wallMetal':        0,
        'acid':             0,
        'triggerDeath':     0,
        'light':            0,
        'exitDoor':         0
    }
    
    for object in objects:
        if object.glpTypes:
            type = object.glpTypes
        else:
            type = "None"
        
        if object.type == "LAMP":
            result['light'] += 1
        elif object.type == "CAMERA":
            result['camera'] += 1
        elif object.type == "MESH":
            if type == "door":
                result['exitDoor'] += 1
            elif type == "trigger":
                if object.glpTriggerTypes == "death":
                    result['triggerDeath'] += 1
            elif type == "wall":
                if object.glpWallTypes == "portalable":
                    result['wallPortalable'] += 1
                else:
                    result['wallMetal'] += 1
            elif type == "volume":
                if object.glpVolumeTypes == "acid":
                    result['acid'] += 1
    
    return result

class checkMapDialog(bpy.types.Operator):
    bl_idname = "object.map_check_dialog"
    bl_label = "Check map results"
    
    # define properties for popup dialog
    camera = bpy.props.IntProperty (name = "Number of cameras")
    light = bpy.props.IntProperty (name = "Number of lights")
    wallPortalable = bpy.props.IntProperty (name = "Number of portalable wall")
    wallMetal = bpy.props.IntProperty (name = "Number of metal wall")
    exitDoor = bpy.props.IntProperty (name = "Number of exit doors")
    
    def execute(self, context):
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, 400)
    
    def draw(self, context):
        result = countObjects(context)
        layout = self.layout
        error = False
        
        if result['exitDoor'] != 1:
            self.exitDoor = result['exitDoor']
            error = True
            
            layout.prop(self, "exitDoor")
            layout.label(text = "There aren't an exit door, use it only once.", icon = 'CANCEL')
        if result['camera'] != 1:
            self.camera = result['camera']
            error = True
            
            layout.prop(self, "camera")
            layout.label(text = "We are using object camera for spawn position, use it only once.",icon = 'ERROR')
        if result['light'] == 0:
            error = True
            
            layout.label(text = "There isn't a light in the map. You have to add some lights.", icon = 'CANCEL')
        elif result['light'] > 5:
            self.light = result['light']
            error = True
            
            layout.prop(self, "light")
            layout.label(text = "There is too many lights in the map.", icon = 'INFO')
            layout.label(text = "We are sorry but we have some performance issues with lights.")
        if result['wallPortalable'] == 0:
            self.wallPortalable = result['wallPortalable']
            error = True
            
            layout.prop(self, "wallPortalable")
            layout.label(text = "There isn't a portalable wall.", icon = 'ERROR')
        if result['wallMetal'] == 0:
            self.wallMetal = result['wallMetal']
            error = True
            
            layout.prop(self, "wallMetal")
            layout.label(text = "There isn't a metal wall.", icon = 'INFO')
        if result['triggerDeath'] != result['acid']:
            error = True
            
            layout.label(text = "We have some implementation problems.", icon = 'INFO')
            layout.label(text = "Use death trigger for each volume of acid in the map.")
        
        if not error:
            layout.label(text = "Nice work, there isn't an error or a warning in the map", icon = 'FILE_TICK')
