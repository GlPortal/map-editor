import bpy
import os
import bmesh

def resetTriggerSettings(object):
  if object.glpTypes and object.glpTypes == "trigger":
    object.glpTriggerTypes = "none"
    object.draw_type = "TEXTURED"
    object.show_x_ray = False
    object.show_bounds = False
    object.draw_bounds_type = "BOX"

def setTrigger(object, type):
  prefs = bpy.context.user_preferences.addons[__package__].preferences
  clearGlpProperties(object)

  object.glpTypes = "trigger"
  object.glpTriggerTypes = type
  object.draw_type = "WIRE"
  object.show_x_ray = prefs.triggerXrays
  object.show_bounds = True
  object.draw_bounds_type = "CAPSULE"

def fixDoorTexture(me):
  bm = bmesh.new()
  bm.from_mesh(me)

  if hasattr(bm.faces, "ensure_lookup_table"):
    bm.faces.ensure_lookup_table()

  uv_layer = bm.loops.layers.uv[0]

  bm.faces[7].loops[0][uv_layer].uv = (0.5, 0.5)
  bm.faces[7].loops[1][uv_layer].uv = (0.5, 0)
  bm.faces[7].loops[2][uv_layer].uv = (0.5, 0)

  bm.faces[25].loops[0][uv_layer].uv = (0.5, 0.5)
  bm.faces[25].loops[1][uv_layer].uv = (0.5, 0)
  bm.faces[25].loops[2][uv_layer].uv = (0.5, 0)

  bm.to_mesh(me)
  bm.free()

def clearGlpProperties(object):
  object.glpTypes = "none"
  object.glpVolumeTypes = "none"
  object.glpTriggerTypes = "none"
  object.glpWallTypes = "none"
