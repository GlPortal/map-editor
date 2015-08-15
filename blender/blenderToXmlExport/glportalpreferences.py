import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import BoolProperty
from .preferencesHelper import *

class glportalPreferences(AddonPreferences):
    bl_idname = __package__
    
    triggerXrays = BoolProperty (
	name = "Use X-Rays for triggers",
	description = "Enable / Disable X-rays for triggers",
	default = True,
	update = updateTriggerXrays
    )
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "triggerXrays")
