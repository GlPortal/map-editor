import bpy
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ExportHelper

from .Exporter import Exporter

class ExportGlPortalFormat(bpy.types.Operator, ExportHelper):
  bl_idname = "glp.export"
  bl_label = "Export GlPortal XML"
  bl_description = "Export to GlPortal XML file (.xml)"
  bl_options = {'PRESET'}
  filename_ext = ".xml"
  filter_glob = StringProperty(default="*.xml", options={'HIDDEN'})
  mapFormatRadix = BoolProperty(
    name="Map format for Radix",
    description="Export map in format supported by RadixEngine",
    default=False
  )

  def execute(self, context):
    exporter = Exporter(self.filepath)
    exporter.mapFormatRadix = self.mapFormatRadix
    exporter.execute(context)
    bpy.context.window_manager.importedFilepath = self.filepath
    return {'FINISHED'}

  def invoke(self, context, event):
    prefs = bpy.context.user_preferences.addons[__package__].preferences
    self.mapFormatRadix = prefs.mapFormatRadix
    return super().invoke(context, event)
