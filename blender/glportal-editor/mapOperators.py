import bpy
import os
import string
import re
from subprocess import call

from .mapHelpers import *
from .exportglportalformat import *

class fixMap(bpy.types.Operator):
    bl_idname = "wm.fix_map"
    bl_label = "Fix map"
    bl_description = "Fix the map before exporting."
    bl_options = {"UNDO"}

    def execute(self, context):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.transform_apply(rotation=True)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        bpy.ops.object.select_all(action='DESELECT')

        return {'FINISHED'}

class checkMap(bpy.types.Operator):
    bl_idname = "wm.check_map"
    bl_label = "Check map"
    bl_description = "Check the map for problems."

    def execute(self, context):
        bpy.ops.object.map_check_dialog('INVOKE_DEFAULT')

        return {'FINISHED'}

class runGame(bpy.types.Operator):
    bl_idname = "wm.run_game"
    bl_label = "Run game"
    bl_description = "Run game with this map"
    filepath = ""

    def execute(self, context):
        objects = context.scene.objects
        result = countObjects(objects)

        if (result['exitDoor'] == 0 or result['camera'] == 0 or result['light'] == 0 or
                (result['wallPortalable'] == 0 and result['wallMetal'] == 0)):
            bpy.ops.object.map_check_dialog('INVOKE_DEFAULT')
        else:
            addon_prefs = bpy.context.user_preferences.addons[__package__].preferences
            self.filepath = os.path.expanduser("/tmp/glpotal_testmap.xml")

            Exporter.filepath = self.filepath
            Exporter.execute(self, context)

            call([addon_prefs.gameExe, "--datadir", addon_prefs.dataDir, "--mapfrompath", self.filepath])

            os.remove(self.filepath)

        # export map to /tmp
        # launch game with ths map
        # than delete exportet map from data/maps

        return {'FINISHED'}
