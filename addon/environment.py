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
