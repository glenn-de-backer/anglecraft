import bpy

class AngleCraftObjectSettingsPanel(bpy.types.Panel):
    bl_label = "Object Settings"
    bl_idname = "VIEW3D_PT_lora_object"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AngleCraft'

    def draw(self, context):
        layout = self.layout
        params = context.scene.lora_object_settings
        box = layout.box()
        box.prop(params, "object_name")
        box.prop(params, "floor_object_name")


class AngleCraftCameraSphereSettingsPanel(bpy.types.Panel):
    bl_label = "Camera Sphere Settings"
    bl_idname = "VIEW3D_PT_lora_camera_sphere"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AngleCraft'

    def draw(self, context):
        layout = self.layout
        params = context.scene.lora_camera_sphere_settings

        box = layout.box()
        box.prop(params, "sphere_type")

        # Dynamic UI: AI Blueprint vs Standard Distributions
        if params.sphere_type == 'ai_blueprint':
            blueprint_box = box.box()
            blueprint_box.label(text="AI Blueprint Modules", icon='FILE_IMAGE')
            
            blueprint_box.prop(params, "blueprint_cardinals")
            blueprint_box.prop(params, "blueprint_isometrics")
            blueprint_box.prop(params, "blueprint_top_bottom")
            
            # Calculate total views dynamically
            total_views = 0
            if params.blueprint_cardinals: 
                total_views += 4
            if params.blueprint_isometrics: 
                total_views += 4 if params.half_sphere else 8
            if params.blueprint_top_bottom: 
                total_views += 1 if params.half_sphere else 2
                
            blueprint_box.separator()
            blueprint_box.label(text=f"Total Cameras Generated: {total_views}", icon='CAMERA_DATA')
            
            if total_views > 10:
                blueprint_box.label(text="Warning: Exceeds Gemini 10-image limit", icon='ERROR')
        else:
            box.prop(params, "num_cameras_horizontal")
            box.prop(params, "num_cameras_vertical")

        box.prop(params, "half_sphere")
        box.prop(params, "min_radius")
        box.prop(params, "max_radius")

        overlap_box = box.box()
        overlap_box.prop(params, "remove_overlapping")
        if params.remove_overlapping:
            overlap_box.prop(params, "overlap_threshold")
            
        box.prop(params, "random_seed")


class AngleCraftEnvironmentSettingsPanel(bpy.types.Panel):
    bl_label = "Environment Settings"
    bl_idname = "VIEW3D_PT_lora_environment"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AngleCraft'

    def draw(self, context):
        layout = self.layout
        params = context.scene.lora_render_settings

        box = layout.box()
        box.prop(params, "hdri_folder")
        box.prop(params, "override_world")
        if params.override_world:
            box.prop(params, "frames_per_hdri")


class AngleCraftActionsButtonPanel(bpy.types.Panel):
    bl_label = "Actions"
    bl_idname = "VIEW3D_PT_lora_render_button"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AngleCraft'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        params = scene.lora_render_button_settings
        box = layout.box()
        
        target_selected = bool(scene.lora_object_settings.object_name)
        cameras_exist = any(camera for camera in bpy.data.objects if camera.type == 'CAMERA' and 'AngleCraft_Cam' in camera.name)

        row = box.row()
        row.enabled = target_selected
        row.operator("object.create_lora_cameras")
        
        row = box.row()
        row.enabled = cameras_exist
        row.operator("object.delete_lora_cameras")

        # Global Preview Toggle
        preview_col = bpy.data.collections.get("AngleCraft_Preview")
        if preview_col:
            row = box.row()
            is_hidden = preview_col.hide_viewport
            toggle_text = "Show Preview Guides" if is_hidden else "Hide Preview Guides"
            toggle_icon = 'HIDE_ON' if is_hidden else 'HIDE_OFF'
            row.prop(preview_col, "hide_viewport", text=toggle_text, icon=toggle_icon, toggle=True)

        info_box = layout.box()
        info_box.label(text=f"Total Frames: {params.info_num_cameras}", icon='INFO')
        
        if cameras_exist:
            info_box.label(text="Use Render Animation (Ctrl+F12)", icon='RENDER_ANIMATION')