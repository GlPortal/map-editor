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

  def execute(self, context):
    exporter = Exporter(self.filepath)
    exporter.execute(context)
    bpy.context.window_manager.importedFilepath = self.filepath
    return {'FINISHED'}
