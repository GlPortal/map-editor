import bpy

def updateTriggerXrays(self, context):
    addon_prefs = context.user_preferences.addons[__package__].preferences
    triggerXrays = addon_prefs.triggerXrays
    objects = context.scene.objects
    
    for object in objects:
        if object.glpTypes and object.glpTypes == "trigger":
            object.show_x_ray = addon_prefs.triggerXrays
