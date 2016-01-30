import bpy

from .managers import MaterialManager

class ObjectPanel(bpy.types.Panel):
  bl_label = "GlPortal"
  bl_space_type = 'PROPERTIES'
  bl_region_type = 'WINDOW'
  bl_context = "object"

  @classmethod
  def poll(self, context):
    if context.object.glpTypes != "none":
      return True
    return False

  def draw(self, context):
    object = context.active_object
    layout = self.layout
    row = layout.row()

    layout.prop(object, "glpTypes")
    if object.glpTypes == "trigger":
      layout.prop(object, "glpTriggerTypes")
    elif object.glpTypes == "volume":
      layout.prop(object, "glpVolumeTypes")

    if object.glpMaterial != "none":
      mat = MaterialManager.materials[object.glpMaterial]

      layout.label(text="Material properties", icon='MATERIAL')

      row = layout.row(align=True)
      row.alignment = 'EXPAND'
      row.label(text="Name : ")
      row.label(text=mat['fancyname'])

      row = layout.row(align=True)
      row.alignment = 'EXPAND'
      row.label(text="Portalable : ")
      if mat['portalable']:
        row.label(text='Yes')
      else:
        row.label(text='No')

      row = layout.row(align=True)
      row.alignment = 'EXPAND'
      row.label(text="Kind : ")
      row.label(text=mat['kind'])
