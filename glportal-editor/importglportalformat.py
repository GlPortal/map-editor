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
  withoutMaterial = BoolProperty(default=False, name="Objects without material")

  def execute(self, context):
    importer = Importer(self.filepath, self.deleteWorld)
    importer.withoutMaterial = self.withoutMaterial
    importer.execute(context)
    return {'FINISHED'}
