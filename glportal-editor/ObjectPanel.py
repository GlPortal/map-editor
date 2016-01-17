import bpy

class ObjectPanel(bpy.types.Panel):
  bl_label = "GlPortal"
  bl_space_type = 'PROPERTIES'
  bl_region_type = 'WINDOW'
  bl_context = "object"

  def draw(self, context):
    object = context.active_object
    layout = self.layout
    row = layout.row()

    if object.glpTypes != "none":
      layout.prop(object, "glpTypes")
      if object.glpTypes == "trigger":
        layout.prop(object, "glpTriggerTypes")
      elif object.glpTypes == "wall":
        layout.prop(object, "glpWallTypes")
      elif object.glpTypes == "volume":
        layout.prop(object, "glpVolumeTypes")
    else:
      layout.label(text="This is no GlPortal object")
