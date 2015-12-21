import bpy

class GlPortalPanel(bpy.types.Panel):
  bl_label = "Set Type"
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'TOOLS'
  bl_category = "GlPortal"

  def draw(self, context):
    layout = self.layout

    layout.label("Wall:")
    row = layout.row()
    split = layout.split()
    col = split.column(align=True)
    col.operator("wm.set_portalable", icon='MESH_PLANE')
    col.operator("wm.set_wall", icon='META_PLANE')

    layout.label("Volume:")
    row = layout.row()
    split = layout.split()
    col = split.column(align=True)
    col.operator("wm.set_acid", icon='MESH_CUBE')

    layout.label("Trigger:")
    row = layout.row()
    split = layout.split()
    col = split.column(align=True)
    col.operator("wm.set_death", icon='MESH_CUBE')
    col.operator("wm.set_radiation", icon='RADIO')
    col.operator("wm.set_win", icon='MESH_CUBE')

    layout.label("Light:")
    row = layout.row()
    split = layout.split()
    col = split.column(align=True)
    col.operator("wm.set_light_common", icon='LAMP_POINT')
    col.operator("wm.set_light_end", icon='LAMP_POINT')

    layout.label("Map:")
    row = layout.row()
    split = layout.split()
    col = split.column(align=True)
    col.operator("wm.fix_map", icon='SCRIPTWIN')
    col.operator("wm.check_map", icon='QUESTION')
    col.operator("wm.run_game", icon='GAME')
