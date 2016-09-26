import bpy
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper

from .importer import Importer

class ImportGlPortalFormat(bpy.types.Operator, ImportHelper):
  bl_idname = "glp.import"
  bl_label = "Import GlPortal XML"
  bl_description = "Import GlPortal XML file (.xml)"
  bl_options = {'PRESET'}
  filename_ext = ".xml"
  filter_glob = StringProperty(default="*.xml", options={'HIDDEN'})
  deleteWorld = BoolProperty(default=True, name="Erase current scene")
  mapFormatRadix = BoolProperty(
    name = "Map format for Radix",
    description = "Export map in format supported by RadixEngine",
    default = False
  )

  def execute(self, context):
    importer = Importer(self.filepath, self.deleteWorld)
    importer.mapFormatRadix = self.mapFormatRadix
    importer.execute(context)
    bpy.context.window_manager.importedFilepath = self.filepath
    return {'FINISHED'}

  def invoke(self, context, event):
    prefs = bpy.context.user_preferences.addons[__package__].preferences
    self.mapFormatRadix = prefs.mapFormatRadix
    return super().invoke(context, event)
