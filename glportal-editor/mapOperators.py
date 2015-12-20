import bpy
import os
from subprocess import call

from .mapHelpers import *
from .exporter import *

class fixMap(bpy.types.Operator):
  bl_idname = "wm.fix_map"
  bl_label = "Fix map"
  bl_description = "Fix the map before exporting."
  bl_options = {"UNDO"}

  def execute(self, context):
    fixObjects()

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

  def execute(self, context):
    objects = context.scene.objects
    result = countObjects(objects)

    if (result['exitDoor'] == 0 or result['camera'] == 0 or result['light'] == 0 or
        (result['wallPortalable'] == 0 and result['wallMetal'] == 0)):
      bpy.ops.object.map_check_dialog('INVOKE_DEFAULT')
    else:
      prefs = bpy.context.user_preferences.addons[__package__].preferences
      filepath = os.path.expanduser(bpy.app.tempdir + "glpotal_testmap.xml")

      if os.path.isdir(prefs.dataDir):
        if os.path.isfile(prefs.gameExe):
          exporter = Exporter(filepath);
          exporter.execute(context)

          call([prefs.gameExe, "--datadir", prefs.dataDir, "--mapfrompath", filepath])

          os.remove(filepath)
        else:
          self.report({'ERROR'}, "GlPortal executable does not exist.")
      else:
        self.report({'ERROR'}, "GlPortal data directory does not exist.")

    return {'FINISHED'}
