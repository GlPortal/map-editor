import bpy


class SidePanel(bpy.types.Panel):
  bl_label = "Set Type"
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'TOOLS'
  bl_category = "GlPortal"

  def draw(self, context):
    layout = self.layout

    layout.label("Objects:")
    layout.operator("glp.search_material", icon='MATERIAL')

    layout.label("Wall:")
    layout.operator("glp.set_portalable", icon='MESH_PLANE')
    layout.operator("glp.set_wall", icon='META_PLANE')

    layout.label("Volume:")
    layout.operator("glp.set_acid", icon='MESH_CUBE')

    layout.label("Trigger:")
    layout.operator("glp.set_death", icon='MESH_CUBE')
    layout.operator("glp.set_radiation", icon='RADIO')
    layout.operator("glp.set_win", icon='MESH_CUBE')

    layout.label("Light:")
    layout.operator("glp.set_light_common", icon='LAMP_POINT')
    layout.operator("glp.set_light_end", icon='LAMP_POINT')

    layout.label("Map:")
    layout.operator("glp.fix_map", icon='SCRIPTWIN')
    layout.operator("glp.check_map", icon='QUESTION')
    layout.operator("glp.run_game", icon='GAME')
    layout.operator("glp.fast_export", icon='GAME')

    layout.label("Others:")
    layout.operator("glp.reload_materials", icon='SCRIPTWIN')
