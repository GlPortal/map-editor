#!BPY
bl_info = {
  "name":         "GlPortal XML Format",
  "author":       "Henry Hirsch, Julian Thijssen, Juraj Oravec",
  "blender":      (2, 6, 3),
  "version":      (1, 0, 0),
  "location":     "File > Import-Export",
  "description":  "Module for loading, editing and saving GlPortal maps.",
  "category":     "Import-Export",
  "tracker_url":  "https://github.com/GlPortal/map-editor/issues"
}

if "bpy" not in locals():
  from . import types
  from . import CreationPanel
  from . import SidePanel
  from . import ObjectPanel
  from . import exportglportalformat
  from . import importglportalformat
  from . import operators
  from . import triggerOperators
  from . import volumeOperators
  from . import mapOperators
  from . import preferences
  from . import mapHelpers
  from . import glportalMenuAdd
  from . import updateTextures
  from . import lightsOperators
  from . import Exporter
  from . import importer
  from . import operatorHelpers
  from . import preferencesHelper
  from . import MPTypes
  from . import MaterialPanel
  from . import validator
  from .utils import directory
  from .managers import MaterialManager
  from .managers import ModelManager
  from .managers import MapManager
  from .managers import AudioManager
else:
  import importlib

  importlib.reload(types)
  importlib.reload(CreationPanel)
  importlib.reload(SidePanel)
  importlib.reload(ObjectPanel)
  importlib.reload(exportglportalformat)
  importlib.reload(importglportalformat)
  importlib.reload(operators)
  importlib.reload(triggerOperators)
  importlib.reload(volumeOperators)
  importlib.reload(mapOperators)
  importlib.reload(preferences)
  importlib.reload(mapHelpers)
  importlib.reload(glportalMenuAdd)
  importlib.reload(updateTextures)
  importlib.reload(lightsOperators)
  importlib.reload(Exporter)
  importlib.reload(importer)
  importlib.reload(operatorHelpers)
  importlib.reload(preferencesHelper)
  importlib.reload(validator)
  importlib.reload(directory)
  importlib.reload(MaterialManager)
  importlib.reload(ModelManager)
  importlib.reload(MPTypes)
  importlib.reload(MaterialPanel)
  importlib.reload(MapManager)
  importlib.reload(AudioManager)

import bpy
import os


def menu_func_export(self, context):
  self.layout.operator("glp.export", text="GlPortal Map (.xml)")


def menu_func_import(self, context):
  self.layout.operator("glp.import", text="GlPortal Map (.xml)")


def register():
  bpy.utils.register_module(__name__)

  types.setProperties()
  MPTypes.initProperties()

  bpy.types.INFO_MT_file_export.append(menu_func_export)
  bpy.types.INFO_MT_file_import.append(menu_func_import)
  bpy.types.INFO_MT_add.prepend(glportalMenuAdd.glportal_add_menu)
  bpy.app.handlers.scene_update_post.append(updateTextures.sceneUpdater)
  bpy.types.WindowManager.MPMaterials = bpy.props.CollectionProperty(type=MPTypes.Row)

  bpy.types.Scene.countObjects = mapHelpers.countObjects
  bpy.types.Scene.fixObjects = mapHelpers.fixObjects
  bpy.types.Object.isOverObject = mapHelpers.isOverObject
  bpy.types.Object.updateTexture = updateTextures.updateTexture

  os.path.browse = directory.browse

  MaterialManager.preload()
  ModelManager.preload()
  MapManager.preload()
  AudioManager.preload()
  MaterialPanel.initRows()


def unregister():
  bpy.utils.unregister_module(__name__)

  MaterialManager.glpMaterialReset()
  MaterialManager.MATERIALS.clear()
  ModelManager.MODELS.clear()
  types.delProperties()
  MPTypes.delProperties()

  bpy.types.INFO_MT_file_export.remove(menu_func_import)
  bpy.types.INFO_MT_file_export.remove(menu_func_export)
  bpy.types.INFO_MT_add.remove(glportalMenuAdd.glportal_add_menu)
  bpy.app.handlers.scene_update_post.remove(updateTextures.sceneUpdater)

  del bpy.types.Scene.countObjects
  del bpy.types.Scene.fixObjects
  del bpy.types.Object.isOverObject
  del bpy.types.Object.updateTexture

  del os.path.browse

  del bpy.types.WindowManager.MPMaterials


if __name__ == "__main__":
  register()
