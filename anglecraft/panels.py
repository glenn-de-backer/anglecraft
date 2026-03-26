import bpy

# Panel for Object Settings
class AngleCraftObjectSettingsPanel(bpy.types.Panel):
    """
    Panel in the 3D View for setting the object and floor mesh for camera placement.
    """
    bl_label = "Object Settings"
    bl_idname = "VIEW3D_PT_lora_object_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AngleCraft'

    def draw(self, context):
        """Draw the Object Settings panel in the UI."""
        layout = self.layout
        scene = context.scene
        params = scene.lora_object_settings

        box = layout.box()
        box.prop(params, "object_name")
        box.prop(params, "floor_object_name")


# Panel for Camera Sphere Settings
class AngleCraftCameraSphereSettingsPanel(bpy.types.Panel):
    """
    Panel in the 3D View for setting the camera sphere parameters such as radius,
    number of cameras, and distribution type.
    """
    bl_label = "Camera Sphere Settings"
    bl_idname = "VIEW3D_PT_lora_camera_sphere_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AngleCraft'

    def draw(self, context):
        """Draw the Camera Sphere Settings panel in the UI."""
        layout = self.layout
        scene = context.scene
        params = scene.lora_camera_sphere_settings

        box = layout.box()
        
        box.prop(params, "min_radius")
        box.prop(params, "max_radius")
        box.prop(params, "num_cameras_horizontal")
        box.prop(params, "num_cameras_vertical")
        box.prop(params, "sphere_type")
        
        # Disable the half sphere option for 'weighted' and 'equator_dense' sphere types
        row = box.row()
        row.enabled = params.sphere_type not in {'weighted', 'equator_dense'}
        row.prop(params, "half_sphere", text="Half Sphere")
        
        box.prop(params, "remove_overlapping")
        box.prop(params, "overlap_threshold")

        # Expose the random seed property to the UI
        layout.separator()
        box.prop(params, "random_seed")
        
# Panel for Environment Settings
class AngleCraftEnvironmentSettingsPanel(bpy.types.Panel):
    """
    Panel in the 3D View for setting environment-related settings such as HDRI.
    """
    bl_label = "Environment Settings"
    bl_idname = "VIEW3D_PT_lora_environment_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AngleCraft'

    def draw(self, context):
        """Draw the Environment Settings panel in the UI."""
        layout = self.layout
        scene = context.scene
        params = scene.lora_render_settings

        box = layout.box()
        
        # Add toggle for overriding world
        box.prop(params, "override_world")
                
        # HDRI folder selection
        box.prop(params, "hdri_folder")

        # Expose the Frames per HDRI property
        box.prop(params, "frames_per_hdri")


# Panel for Actions Button
class AngleCraftActionsButtonPanel(bpy.types.Panel):
    """
    Panel in the 3D View that contains the button to trigger the rendering process.
    """
    bl_label = "Actions"
    bl_idname = "VIEW3D_PT_lora_render_button"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AngleCraft'

    def draw(self, context):
        """Draw the Render Button panel in the UI."""
        layout = self.layout
        scene = context.scene
        params = scene.lora_render_button_settings

        box = layout.box()
        
        # Check if a target empty is selected
        target_selected = bool(context.scene.lora_object_settings.object_name)
        
        # Check if any cameras with '_AngleCraft_Cam' exist
        cameras_exist = any(camera for camera in bpy.data.objects if camera.type == 'CAMERA' and 'AngleCraft_Cam' in camera.name)

        # Create buttons and disable them if no target empty is selected or no cameras exist
        row = box.row()
        row.enabled = target_selected
        row.operator("object.create_lora_cameras")
        
        row = box.row()
        row.enabled = cameras_exist
        row.operator("object.delete_lora_cameras")

        # --- NEW: Global Preview Toggle ---
        preview_col = bpy.data.collections.get("AngleCraft_Preview")
        if preview_col:
            row = box.row()
            # Change text and icon based on visibility state
            is_hidden = preview_col.hide_viewport
            toggle_text = "Show Preview Guides" if is_hidden else "Hide Preview Guides"
            toggle_icon = 'HIDE_ON' if is_hidden else 'HIDE_OFF'
            
            # Using toggle=True makes it look like a nice big button
            row.prop(preview_col, "hide_viewport", text=toggle_text, icon=toggle_icon, toggle=True)

        # Add another box for the label to avoid overlap
        info_box = layout.box()
        info_box.label(text=f"Total Frames: {params.info_num_cameras}", icon='INFO')
        
        # Guide the user to use Blender's native rendering
        if cameras_exist:
            info_box.label(text="Use Render Animation (Ctrl+F12)", icon='RENDER_ANIMATION')