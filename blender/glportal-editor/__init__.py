#!BPY
bl_info = {
    "name":         "GlPortal XML Format",
    "author":       "Henry Hirsch, Julian Thijssen, Juraj Oravec",
    "blender":      (2, 6, 3),
    "version":      (0, 0, 6),
    "location":     "File > Import-Export",
    "description":  "Module for loading, editing and saving GlPortal maps.",
    "category":     "Import-Export",
    "tracker_url":  "https://github.com/GlPortal/tools/issues"
}

import bpy
import xml.etree.cElementTree as tree
import xml.dom.minidom as minidom
import os
import mathutils
import math
import string
from mathutils import Vector
import re
from .glportalcreationpanel import *
from .glportalpanel import *
from .glportalobjectpanel import *
from .exportglportalformat import *
from .importglportalformat import *
from .operators import *
from .triggerOperators import *
from .volumeOperators import *
from .mapOperators import *
from .glportalpreferences import *
from .mapHelpers import *
from .glportalMenuAdd import *
from .updateTextures import *
from .lightsOperators import *

def menu_func_export(self, context):
    self.layout.operator(ExportGlPortalFormat.bl_idname, text="GlPortal Map (.xml)")

def menu_func_import(self, context):
    self.layout.operator(ImportGlPortalFormat.bl_idname, text="GlPortal Map (.xml)")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_export.append(menu_func_export)
    bpy.types.INFO_MT_file_import.append(menu_func_import)
    bpy.types.INFO_MT_add.prepend(glportal_add_menu)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_export.remove(menu_func_import)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)
    bpy.types.INFO_MT_add.remove(glportal_add_menu)

if __name__ == "__main__":
    register()
