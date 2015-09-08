import bpy

class GlPortalPanel(bpy.types.Panel):
    """GlPortal panel in the toolbar"""
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
        col.operator("wm.set_portalable", text="Portalable", icon='MESH_PLANE')
        col.operator("wm.set_wall", text="Tiles", icon='META_PLANE')
        
        layout.label("Volume:")
        row = layout.row()
        split = layout.split()
        col = split.column(align=True)
        col.operator("wm.set_acid", text="Acid", icon='MESH_CUBE')
        
        layout.label("Trigger:")
        row = layout.row()
        split = layout.split()
        col = split.column(align=True)
        col.operator("wm.set_death", text="Death", icon='MESH_CUBE')
        col.operator("wm.set_radiation", text="Radiation", icon='RADIO')
        col.operator("wm.set_win", text="Win", icon='MESH_CUBE')
        
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
        col.operator("wm.fix_map", text="Fix Map", icon='SCRIPTWIN')
        col.operator("wm.check_map", text="Check Map", icon='QUESTION')
