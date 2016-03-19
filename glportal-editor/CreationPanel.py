import bpy

class CreationPanel(bpy.types.Panel):
  bl_label = "GlPortal"
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'TOOLS'
  bl_context = "objectmode"
  bl_category = "Create"

  def draw(self, context):
    layout = self.layout
    layout.label("Objects:")
    layout.operator("glp.add_door", text="Exit", icon='MESH_CUBE')
    layout.operator("glp.search_model", icon='MESH_CUBE')
    layout.operator("glp.search_material", icon='MATERIAL')

    layout.label("Wall:")
    layout.operator("glp.add_portalable", icon='MESH_PLANE')
    layout.operator("glp.add_wall", icon='META_PLANE')

    layout.label("Volume:")
    layout.operator("glp.add_acid", icon='MESH_CUBE')

    layout.label("Trigger:")
    layout.operator("glp.add_death", icon='MESH_CUBE')
    layout.operator("glp.add_radiation", icon='RADIO')
    layout.operator("glp.add_win", icon='MESH_CUBE')

    layout.label("Light:")
    layout.operator("glp.add_light_common", icon='LAMP_POINT')
    layout.operator("glp.add_light_end", icon='LAMP_POINT')

#    layout.label("Models:")
#    row = layout.row()
#    split = layout.split()
#    col = split.column(align=True)
#    col.operator("wm.add_door", text="Door", icon='MESH_CUBE')
#    col.operator("wm.add_lamp", text="Lamp", icon='MESH_CUBE')
#    col.operator("wm.add_button", text="Button", icon='MESH_CUBE')
