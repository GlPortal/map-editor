import bpy
from bpy.props import *
from bpy_extras.io_utils import ImportHelper

from .importer import *

class ImportGlPortalFormat(bpy.types.Operator, ImportHelper):
  bl_idname = "import_glportal_xml.xml"
  bl_label = "Import GlPortal XML"
  bl_description = "Import GlPortal XML file (.xml)"
  bl_options = {'PRESET'}
  filename_ext = ".xml"
  filter_glob = StringProperty(default="*.xml", options={'HIDDEN'})

  def execute(self, context):
    importer = Importer(self.filepath)
    importer.execute(context)

    return {'FINISHED'}
