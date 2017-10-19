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
  deleteWorld = BoolProperty(
    name="Clear scene",
    description="Clear current scene",
    default=True
  )
  asGroup = BoolProperty(
    name="Import as group",
    description="Create group from all objects in imported map",
    default=False
  )

  def execute(self, context):
    importer = Importer()
    importer.filePath = self.filepath
    importer.clearScene = self.deleteWorld
    importer.asGroup = self.asGroup
    importer.execute(context)
    bpy.context.window_manager.importedFilepath = self.filepath
    return {'FINISHED'}
