import bpy
import os
from bpy.types import Operator, AddonPreferences
from bpy.props import BoolProperty, StringProperty
from .preferencesHelper import *

class glportalPreferences(AddonPreferences):
    bl_idname = __package__
    
    triggerXrays = BoolProperty (
        name = "Use X-Rays for triggers",
        description = "Enable / Disable X-rays for triggers",
        default = True,
        update = updateTriggerXrays
    )
    smartTexturesMapping = BoolProperty (
        name = "Smart textures mapping",
        description = "Calculate position of each texture.",
        default = True,
        update = updateSmartTexturesMapping
    )
    dataDir = StringProperty (
        name = "Set up GlPortal data directory",
        default = os.path.expanduser("~/.glportal/data/"),
        subtype = 'DIR_PATH'
    )
    gameExe = StringProperty (
        name = "Set up GlPortal executable",
        default = os.path.expanduser("/usr/bin/glportal"),
        subtype = 'FILE_PATH'
    )
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "triggerXrays")
        layout.prop(self, "smartTexturesMapping")
        layout.prop(self, "dataDir")
        layout.prop(self, "gameExe")
