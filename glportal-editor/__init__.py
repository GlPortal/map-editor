#!BPY
bl_info = {
  "name":         "GlPortal XML Format",
  "author":       "Henry Hirsch, Julian Thijssen, Juraj Oravec",
  "blender":      (2, 6, 3),
  "version":      (1, 0, 0),
  "location":     "File > Import-Export",
  "description":  "Module for loading, editing and saving GlPortal maps.",
  "category":     "Import-Export",
  "tracker_url":  "https://github.com/GlPortal/tools/issues"
}

if "bpy" in locals():
  import importlib

  importlib.reload(types)
  importlib.reload(glportalcreationpanel)
  importlib.reload(glportalpanel)
  importlib.reload(glportalobjectpanel)
  importlib.reload(exportglportalformat)
  importlib.reload(importglportalformat)
  importlib.reload(operators)
  importlib.reload(triggerOperators)
  importlib.reload(volumeOperators)
  importlib.reload(mapOperators)
  importlib.reload(glportalpreferences)
  importlib.reload(mapHelpers)
  importlib.reload(glportalMenuAdd)
  importlib.reload(updateTextures)
  importlib.reload(lightsOperators)
  importlib.reload(exporter)
  importlib.reload(operatorHelpers)
  importlib.reload(preferencesHelper)
else:
  from . import types
  from . import glportalcreationpanel
  from . import glportalpanel
  from . import glportalobjectpanel
  from . import exportglportalformat
  from . import importglportalformat
  from . import operators
  from . import triggerOperators
  from . import volumeOperators
  from . import mapOperators
  from . import glportalpreferences
  from . import mapHelpers
  from . import glportalMenuAdd
  from . import updateTextures
  from . import lightsOperators
  from . import exporter
  from . import operatorHelpers
  from . import preferencesHelper

import bpy
import xml.etree.cElementTree as tree
import xml.dom.minidom as minidom
import os
import mathutils
import math
import string
from mathutils import Vector
import re

def menu_func_export(self, context):
  self.layout.operator(exportglportalformat.ExportGlPortalFormat.bl_idname, text="GlPortal Map (.xml)")

def menu_func_import(self, context):
  self.layout.operator(importglportalformat.ImportGlPortalFormat.bl_idname, text="GlPortal Map (.xml)")

def register():
  bpy.utils.register_module(__name__)
  bpy.types.INFO_MT_file_export.append(menu_func_export)
  bpy.types.INFO_MT_file_import.append(menu_func_import)
  bpy.types.INFO_MT_add.prepend(glportalMenuAdd.glportal_add_menu)
  bpy.app.handlers.scene_update_post.append(updateTextures.sceneUpdater)

def unregister():
  bpy.utils.unregister_module(__name__)
  bpy.types.INFO_MT_file_export.remove(menu_func_import)
  bpy.types.INFO_MT_file_export.remove(menu_func_export)
  bpy.types.INFO_MT_add.remove(glportalMenuAdd.glportal_add_menu)
  bpy.app.handlers.scene_update_post.remove(updateTextures.sceneUpdater)

if __name__ == "__main__":
  register()
