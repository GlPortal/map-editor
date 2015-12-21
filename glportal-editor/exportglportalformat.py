import bpy
from bpy.props import *
from bpy_extras.io_utils import ExportHelper

from .Exporter import *

class ExportGlPortalFormat(bpy.types.Operator, ExportHelper):
  bl_idname = "export_glportal_xml.xml"
  bl_label = "Export GlPortal XML"
  bl_description = "Export to GlPortal XML file (.xml)"
  bl_options = {'PRESET'}
  filename_ext = ".xml"
  filter_glob = StringProperty(default="*.xml", options={'HIDDEN'})

  def execute(self, context):
    exporter = Exporter(self.filepath)
    exporter.execute(context)

    return {'FINISHED'}
