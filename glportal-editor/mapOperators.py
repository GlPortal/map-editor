import bpy
import os
from subprocess import call

from .Exporter import Exporter
from .managers import MaterialManager


class FixMaterials(bpy.types.Operator):
  bl_idname = "glp.fix_materials"
  bl_label = "Fix materials"
  bl_description = "Assign default material to objects without it."
  bl_options = {'UNDO'}

  def execute(self, context):
    prefs = bpy.context.user_preferences.addons[__package__].preferences
    material = prefs.defaultMaterial
    objects = context.scene.objects

    for object in objects:
      if object.type == 'MESH' and object.glpTypes in {"model", "wall"}:
        if not object.glpMaterial or object.glpMaterial == "none":
          object.glpMaterial = material

    return {'FINISHED'}


class ReloadMaterials(bpy.types.Operator):
  bl_idname = "glp.reload_materials"
  bl_label = "Reload materials"
  bl_description = "Reload GlPortal materials"

  def execute(self, context):
    MaterialManager.reload()
    return {'FINISHED'}


class FastExport(bpy.types.Operator):
  bl_idname = "glp.fast_export"
  bl_label = "Fast Export"
  bl_description = "Export current map to the imported file"

  def execute(self, context):
    filepath = bpy.context.window_manager.importedFilepath

    if filepath != "none":
      if os.path.isfile(filepath):
        exporter = Exporter(filepath)
        exporter.execute(context)

        self.report({'INFO'}, "Map exported")
      else:
        self.report({'ERROR'}, "Filepath does not exist")
    else:
      self.report({'ERROR'}, "Filepath is empty")

    return {'FINISHED'}


class FixMap(bpy.types.Operator):
  bl_idname = "glp.fix_map"
  bl_label = "Fix map"
  bl_description = "Fix the map before exporting."
  bl_options = {'UNDO'}

  def execute(self, context):
    bpy.context.scene.fixObjects()
    bpy.ops.glp.fix_materials()
    return {'FINISHED'}


class CheckMap(bpy.types.Operator):
  bl_idname = "glp.check_map"
  bl_label = "Check map"
  bl_description = "Check the map for problems."

  def execute(self, context):
    bpy.ops.object.map_check_dialog('INVOKE_DEFAULT')
    return {'FINISHED'}


class RunGame(bpy.types.Operator):
  bl_idname = "glp.run_game"
  bl_label = "Run game"
  bl_description = "Run game with this map"

  def execute(self, context):
    result = context.scene.countObjects()

    if (
      result["exitDoor"] == 0 or
      result["camera"] == 0 or
      result["light"] == 0 or
      result["wall"] == 0
    ):
      bpy.ops.object.map_check_dialog('INVOKE_DEFAULT')
    else:
      prefs = bpy.context.user_preferences.addons[__package__].preferences
      filepath = os.path.join(bpy.app.tempdir, "glportal_testmap.xml")

      if os.path.isdir(prefs.dataDir):
        if os.path.isfile(prefs.gameExe):
          exporter = Exporter(filepath)
          exporter.execute(context)

          call(
            [prefs.gameExe, "--datadir", prefs.dataDir, "--mapfrompath", filepath],
            env=os.environ
          )

          os.remove(filepath)
        else:
          self.report({'ERROR'}, "GlPortal executable does not exist.")
      else:
        self.report({'ERROR'}, "GlPortal data directory does not exist.")
    return {'FINISHED'}
