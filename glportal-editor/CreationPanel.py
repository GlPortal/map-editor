import bpy

class CreationPanel(bpy.types.Panel):
  bl_label = "GlPortal"
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'TOOLS'
  bl_context = "objectmode"
  bl_category = "Create"

  def draw(self, context):
    layout = self.layout
    layout.label("Object:")
    row = layout.row()
    split = layout.split()
    col = split.column(align=True)
    col.operator("glp.add_door", text="Exit", icon='MESH_CUBE')

    layout.label("Wall:")
    row = layout.row()
    split = layout.split()
    col = split.column(align=True)
    col.operator("glp.add_portalable", icon='MESH_PLANE')
    col.operator("glp.add_wall", icon='META_PLANE')

    layout.label("Volume:")
    row = layout.row()
    split = layout.split()
    col = split.column(align=True)
    col.operator("glp.add_acid", icon='MESH_CUBE')

    layout.label("Trigger:")
    row = layout.row()
    split = layout.split()
    col = split.column(align=True)
    col.operator("glp.add_death", icon='MESH_CUBE')
    col.operator("glp.add_radiation", icon='RADIO')
    col.operator("glp.add_win", icon='MESH_CUBE')

    layout.label("Light:")
    row = layout.row()
    split = layout.split()
    col = split.column(align=True)
    col.operator("glp.add_light_common", icon='LAMP_POINT')
    col.operator("glp.add_light_end", icon='LAMP_POINT')

#    layout.label("Models:")
#    row = layout.row()
#    split = layout.split()
#    col = split.column(align=True)
#    col.operator("wm.add_door", text="Door", icon='MESH_CUBE')
#    col.operator("wm.add_lamp", text="Lamp", icon='MESH_CUBE')
#    col.operator("wm.add_button", text="Button", icon='MESH_CUBE')
