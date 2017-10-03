import bpy


class SidePanel(bpy.types.Panel):
  bl_label = "Set Type"
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'TOOLS'
  bl_category = "GlPortal"

  def draw(self, context):
    layout = self.layout

    layout.label("Objects:")
    layout.operator("glp.manager_search_set_material", icon='MATERIAL')

    layout.label("Wall:")
    layout.operator("glp.wall_set_portalable", icon='MESH_PLANE', text="Portalable")
    layout.operator("glp.wall_set_metal", icon='META_PLANE', text="Metal")

    layout.label("Volume:")
    layout.operator("glp.volume_set_acid", icon='MESH_CUBE', text="Acid")

    layout.label("Trigger:")
    layout.operator("glp.trigger_set_death", icon='MESH_CUBE', text="Death")
    layout.operator("glp.trigger_set_radiation", icon='RADIO')
    layout.operator("glp.trigger_set_win", icon='MESH_CUBE', text="Win")
    layout.operator("glp.trigger_search_map", icon='MESH_CUBE', text="Map")
    layout.operator("glp.trigger_search_audio", icon='MESH_CUBE', text="Audio")

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
