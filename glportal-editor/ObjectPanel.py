import bpy

from .managers import MaterialManager


class ObjectPanel(bpy.types.Panel):
  bl_label = "GlPortal"
  bl_space_type = 'PROPERTIES'
  bl_region_type = 'WINDOW'
  bl_context = "object"

  @classmethod
  def poll(cls, context):
    if context.object.glpTypes != "none":
      return True
    return False

  def draw(self, context):
    object = context.active_object
    layout = self.layout

    layout.prop(object, "glpTypes")
    if object.glpTypes == "trigger":
      layout.prop(object, "glpTriggerTypes")

      if object.glpTriggerTypes in {"map", "audio"}:
        layout.prop(object, "glpTriggerFilepath")

        if object.glpTriggerTypes == "audio":
          layout.prop(object, "glpTriggerAudioLoop")
    elif object.glpTypes == "volume":
      layout.prop(object, "glpVolumeTypes")

    if object.glpMaterial:
      layout.label(text="Material properties", icon='MATERIAL')

      layout.prop(object, "glpMaterial", text="Name ")

      if object.glpMaterial != "none":
        mat = MaterialManager.MATERIALS[object.glpMaterial]

        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.label(text="Portalable : ")
        if mat['portalable']:
          row.label(text="Yes")
        else:
          row.label(text="No")

        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.label(text="Kind : ")
        row.label(text=mat["kind"])
