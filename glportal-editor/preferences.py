import bpy
import os
from bpy.types import AddonPreferences
from bpy.props import BoolProperty, EnumProperty, StringProperty

from .operatorHelpers import itemsMaterial
from .preferencesHelper import updateTriggerXrays, updateDefaultMaterial, updateDataDir
from .managers import MaterialManager as MM

class preferences(AddonPreferences):
  bl_idname = __package__

  triggerXrays = BoolProperty (
    name = "Use X-Rays for triggers",
    description = "Enable / Disable X-rays for triggers.",
    default = True,
    update = updateTriggerXrays
  )
  dataDir = StringProperty (
    name = "Set up GlPortal data directory",
    default = os.path.expanduser("~/.glportal/data/"),
    subtype = 'DIR_PATH',
    update = updateDataDir
  )
  gameExe = StringProperty (
    name = "Set up GlPortal executable",
    default = os.path.expanduser("/usr/bin/glportal"),
    subtype = 'FILE_PATH'
  )
  defaultMaterial = StringProperty (
    default = "boxes/dev00"
  )
  materials = EnumProperty (
    name = "Default material",
    items = itemsMaterial,
    update = updateDefaultMaterial
  )
  mapFormatRadix = BoolProperty(
    name = "Map format for Radix",
    description = "Export map in format supported by RadixEngine",
    default = False
  )

  def draw(self, context):
    layout = self.layout

    layout.prop(self, "triggerXrays")
    layout.prop(self, "mapFormatRadix")

    if len(MM.materials) > 1:
      if self.defaultMaterial not in MM.materials:
        self.materials = self.defaultMaterial

        layout.label(text="Default material is not on the list.", icon='ERROR')
    else:
      layout.label(text="Material list is empty", icon='ERROR')
    layout.prop(self, "materials")

    layout.prop(self, "dataDir")
    if os.path.isdir(os.path.expanduser(self.dataDir)) == False:
      layout.label(text="Current data directory does not exist", icon='ERROR')

    layout.prop(self, "gameExe")
    if os.path.isfile(os.path.expanduser(self.gameExe)) == False:
      layout.label(text="Current GlPortal executable does not exist", icon='ERROR')
