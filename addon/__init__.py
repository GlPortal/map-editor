#!BPY
bl_info = {
  "name":         "Radix Map Editor",
  "author":       "Henry Hirsch, Julian Thijssen, Juraj Oravec",
  "blender":      (2, 6, 3),
  "version":      (1, 0, 0),
  "location":     "File > Import-Export",
  "description":  "Module for loading, editing and saving Radix maps.",
  "category":     "Import-Export",
  "tracker_url":  "https://github.com/GlPortal/map-editor/issues"
}

if "bpy" not in locals():
  from . import types
  from . import exportRadixFormat
  from . import importRadixFormat
  from . import operatorsList
  from . import OperatorManager
  from . import mapOperators
  from . import preferences
  from . import mapHelpers
  from . import radixMenuAdd
  from . import updateTextures
  from . import lightsOperators
  from . import Exporter
  from . import importer
  from . import operatorHelpers
  from . import preferencesHelper
  from . import MPTypes
  from . import MaterialPanel
  from .utils import directory
  from .managers import MaterialManager
  from .managers import ModelManager
  from .managers import MapManager
  from .managers import AudioManager
  from . import CreationPanel
  from . import SidePanel
  from . import ObjectPanel
else:
  import importlib

  importlib.reload(types)
  importlib.reload(exportRadixFormat)
  importlib.reload(importRadixFormat)
  importlib.reload(operatorsList)
  importlib.reload(operators)
  importlib.reload(mapOperators)
  importlib.reload(preferences)
  importlib.reload(mapHelpers)
  importlib.reload(radixMenuAdd)
  importlib.reload(updateTextures)
  importlib.reload(lightsOperators)
  importlib.reload(Exporter)
  importlib.reload(importer)
  importlib.reload(operatorHelpers)
  importlib.reload(preferencesHelper)
  importlib.reload(directory)
  importlib.reload(MaterialManager)
  importlib.reload(ModelManager)
  importlib.reload(MPTypes)
  importlib.reload(MaterialPanel)
  importlib.reload(MapManager)
  importlib.reload(AudioManager)
  importlib.reload(CreationPanel)
  importlib.reload(SidePanel)
  importlib.reload(ObjectPanel)

import bpy
blender = bpy
import os


def exportMenuOperator(self, context):
  self.layout.operator("radix.export", text="Radix Map (.xml)")


def importMenuOperator(self, context):
  self.layout.operator("radix.import", text="Radix Map (.xml)")

def addMenuItems():
  types = blender.types
  types.INFO_MT_file_export.append(exportMenuOperator)
  types.INFO_MT_file_import.append(importMenuOperator)
  types.INFO_MT_add.prepend(radixMenuAdd.radix_add_menu)

def removeMenuItems():
  types = blender.types
  types.INFO_MT_file_import.remove(importMenuOperator)
  types.INFO_MT_file_export.remove(exportMenuOperator)
  types.INFO_MT_add.remove(radixMenuAdd.radix_add_menu)


def register():
  blender.utils.register_module(__name__)

  types.setProperties()
  MPTypes.initProperties()
  addMenuItems()
  blender.app.handlers.scene_update_post.append(updateTextures.sceneUpdater)
  blender.types.WindowManager.MPMaterials = bpy.props.CollectionProperty(type=MPTypes.Row)
  blenderScene = blender.types.Scene
  blenderScene.countObjects = mapHelpers.countObjects
  blenderScene.fixObjects = mapHelpers.fixObjects
  blenderObject = blender.types.Object
  blenderObject.isOverObject = mapHelpers.isOverObject
  blenderObject.updateTexture = updateTextures.updateTexture
  os.path.browse = directory.browse

  MaterialManager.preload()
  ModelManager.preload()
  MapManager.preload()
  AudioManager.preload()
  MaterialPanel.initRows()

  OperatorManager.addOperators()


def unregister():
  blender.utils.unregister_module(__name__)

  OperatorManager.removeOperators()

  MaterialManager.radixMaterialReset()
  MaterialManager.MATERIALS.clear()
  ModelManager.MODELS.clear()
  types.delProperties()
  MPTypes.delProperties()

  removeMenuItems()
  blender.app.handlers.scene_update_post.remove(updateTextures.sceneUpdater)

  del blender.types.Scene.countObjects
  del blender.types.Scene.fixObjects
  del blender.types.Object.isOverObject
  del blender.types.Object.updateTexture

  del os.path.browse

  del blender.types.WindowManager.MPMaterials


if __name__ == "__main__":
  register()
