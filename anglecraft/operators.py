import bpy
import math
from mathutils import Vector
import os
import random
from bpy.app.handlers import persistent

# -------------------------------------------------------------------
# FRAME HANDLER
# -------------------------------------------------------------------
@persistent
def anglecraft_hdri_handler(scene, depsgraph=None):
    """
    Runs automatically on every frame change. 
    Handles HDRI swapping dynamically and safely creates missing nodes.
    """
    settings = scene.lora_render_settings
    hdri_folder = bpy.path.abspath(settings.hdri_folder)
    override_world = settings.override_world
    
    # Abort if no folder, or if we have a World but Override is unchecked
    if not hdri_folder or not os.path.exists(hdri_folder):
        return
    if scene.world and not override_world:
        return

    hdri_files = [f for f in os.listdir(hdri_folder) if f.lower().endswith(('.hdr', '.exr'))]
    
    if hdri_files:
        frames_per = max(1, settings.frames_per_hdri)
        current_frame = scene.frame_current
        
        # Pick HDRI based on frame pacing
        index = (current_frame // frames_per) % len(hdri_files)
        hdri_filename = hdri_files[index]
        selected_hdri_path = os.path.join(hdri_folder, hdri_filename)

        # 1. Ensure World exists
        if not scene.world:
            scene.world = bpy.data.worlds.new("AngleCraft_World")
            
        scene.world.use_nodes = True
        nodes = scene.world.node_tree.nodes
        links = scene.world.node_tree.links

        # 2. Ensure Environment Texture node exists (Auto-create if missing)
        env_node = next((node for node in nodes if node.type == 'TEX_ENVIRONMENT'), None)
        if not env_node:
            env_node = nodes.new(type="ShaderNodeTexEnvironment")
            bg_node = next((node for node in nodes if node.type == 'BACKGROUND'), None)
            if bg_node:
                links.new(env_node.outputs['Color'], bg_node.inputs['Color'])

        # 3. Safely load and swap the image
        if env_node:
            # Try to grab it from memory first (fastest)
            img = bpy.data.images.get(hdri_filename)
            
            # If it's not in memory yet, load it from the hard drive! (Fallback)
            if not img:
                img = bpy.data.images.load(selected_hdri_path)
                
            # Only trigger an update if the image is actually different
            if env_node.image != img:
                env_node.image = img

# -------------------------------------------------------------------
# MATH & DISTRIBUTION FUNCTIONS
# -------------------------------------------------------------------
def generate_sphere_points(num_horizontal, num_vertical, radius, hemisphere=None):
    points = []
    if num_horizontal <= 0 or num_vertical <= 0: return points

    for i in range(num_vertical):
        if hemisphere == 'top':
            vertical_angle = (math.pi / 2) * (i / (num_vertical - 1))  
        elif hemisphere == 'bottom':
            vertical_angle = (math.pi / 2) * (i / (num_vertical - 1)) + math.pi / 2  
        else:
            vertical_angle = math.pi * i / (num_vertical - 1)  
        
        for j in range(num_horizontal):
            horizontal_angle = 2 * math.pi * j / num_horizontal  
            x = radius * math.sin(vertical_angle) * math.cos(horizontal_angle)
            y = radius * math.sin(vertical_angle) * math.sin(horizontal_angle)
            z = radius * math.cos(vertical_angle)
            points.append((x, y, z))
    return points

def weighted_distribution(num_cameras_total, bias_ratio=0.8):
    top_cameras = int(num_cameras_total * bias_ratio)
    bottom_cameras = num_cameras_total - top_cameras

    num_horizontal_top = int(math.ceil(math.sqrt(top_cameras)))
    num_vertical_top = int(math.ceil(top_cameras / num_horizontal_top))
    num_horizontal_bottom = int(math.ceil(math.sqrt(bottom_cameras)))
    num_vertical_bottom = int(math.ceil(bottom_cameras / num_horizontal_bottom))

    top_sphere_points = generate_sphere_points(num_horizontal_top, num_vertical_top, radius=1.0, hemisphere='top')
    bottom_sphere_points = generate_sphere_points(num_horizontal_bottom, num_vertical_bottom, radius=1.0, hemisphere='bottom')

    return top_sphere_points[:top_cameras] + bottom_sphere_points[:bottom_cameras]

def fibonacci_sphere(samples=1, radius=1.0, half_sphere=False, seed=0):
    points = []
    phi = math.pi * (3. - math.sqrt(5.))
    random.seed(seed)
    offset = random.random() * 2 * math.pi

    for i in range(samples):
        z = 1 - (i / float(samples - 1)) * 2  
        if half_sphere and z < 0: continue  
        
        radius_z = math.sqrt(1 - z * z)  
        theta = (phi * i) + offset  

        x = math.cos(theta) * radius_z
        y = math.sin(theta) * radius_z
        points.append((x * radius, y * radius, z * radius))
    return points

def linear_distribution(num_cameras_horizontal, num_cameras_vertical, radius, half_sphere=False):
    points = []
    for v in range(num_cameras_vertical):
        if half_sphere:
            vertical_angle = (math.pi / 2) * (v / (num_cameras_vertical - 1))  
        else:
            vertical_angle = math.pi * (v + 1) / (num_cameras_vertical + 1)  

        for h in range(num_cameras_horizontal):
            horizontal_angle = (2 * math.pi / num_cameras_horizontal) * h
            x = radius * math.sin(vertical_angle) * math.cos(horizontal_angle)
            y = radius * math.sin(vertical_angle) * math.sin(horizontal_angle)
            z = radius * math.cos(vertical_angle)
            points.append((x, y, z))
    return points

def uniform_distribution(num_cameras_horizontal, num_cameras_vertical, radius, half_sphere=False):
    points = []
    for v in range(num_cameras_vertical):
        if half_sphere:
            vertical_angle = math.acos(1 - 2 * v / (num_cameras_vertical - 1)) / 2
        else:
            vertical_angle = math.acos(1 - 2 * (v + 1) / (num_cameras_vertical + 1))

        for h in range(num_cameras_horizontal):
            horizontal_angle = (2 * math.pi / num_cameras_horizontal) * h
            x = radius * math.sin(vertical_angle) * math.cos(horizontal_angle)
            y = radius * math.sin(vertical_angle) * math.sin(horizontal_angle)
            z = radius * math.cos(vertical_angle)
            points.append((x, y, z))
    return points

def equator_dense_distribution(num_cameras_horizontal, num_cameras_vertical, radius, half_sphere=False):
    points = []
    for v in range(num_cameras_vertical):
        t = (v + 0.5) / num_cameras_vertical  
        if half_sphere:
            vertical_angle = math.asin(t) * (math.pi / 2)  
        else:
            vertical_angle = math.asin(2 * t - 1) + (math.pi / 2)  

        for h in range(num_cameras_horizontal):
            horizontal_angle = (2 * math.pi / num_cameras_horizontal) * h
            x = radius * math.sin(vertical_angle) * math.cos(horizontal_angle)
            y = radius * math.sin(vertical_angle) * math.sin(horizontal_angle)
            z = radius * math.cos(vertical_angle)
            points.append((x, y, z))
    return points

# --- NEW: AI Blueprint Distribution ---
def ai_blueprint_distribution(radius, half_sphere=False):
    """Generates the ideal views for Image-to-Image AI models (Vizcom, Gemini, etc.)"""
    points = []

    # 1. Cardinal Views (Equator / Horizon)
    points.append((0, -radius, 0))  # Front (-Y)
    points.append((radius, 0, 0))   # Right (+X)
    points.append((0, radius, 0))   # Back (+Y)
    points.append((-radius, 0, 0))  # Left (-X)

    # 2. Isometric Top Views (45-degree elevation 3/4 views)
    z_elev = radius * 0.7071 # sin(45)
    xy_radius = radius * 0.7071 # cos(45)
    xy_offset = xy_radius * 0.7071 # 45 degrees on the XY plane

    points.append((xy_offset, -xy_offset, z_elev))  # Top Front-Right
    points.append((xy_offset, xy_offset, z_elev))   # Top Back-Right
    points.append((-xy_offset, xy_offset, z_elev))  # Top Back-Left
    points.append((-xy_offset, -xy_offset, z_elev)) # Top Front-Left

    # 3. Top View
    points.append((0, 0, radius))

    # 4. Bottom and Isometric Bottom Views (If not half sphere)
    if not half_sphere:
        points.append((0, 0, -radius)) # Bottom
        points.append((xy_offset, -xy_offset, -z_elev))  # Bottom Front-Right
        points.append((xy_offset, xy_offset, -z_elev))   # Bottom Back-Right
        points.append((-xy_offset, xy_offset, -z_elev))  # Bottom Back-Left
        points.append((-xy_offset, -xy_offset, -z_elev)) # Bottom Front-Left

    return points

def remove_overlapping_cameras(points, threshold):
    filtered_points = []
    for point in points:
        point_vec = Vector(point)
        if all((point_vec - Vector(other)).length >= threshold for other in filtered_points):
            filtered_points.append(point_vec)
    return filtered_points

# -------------------------------------------------------------------
# CORE GENERATION FUNCTION
# -------------------------------------------------------------------
def create_cameras(object_name, min_radius, max_radius, num_cameras_horizontal, num_cameras_vertical, distribution_type="fibonacci", half_sphere=False, remove_overlapping=False, overlap_threshold=0.1, seed=0):
    """
    Sets up a single animated camera around a target object based on the selected distribution.
    """
    scene = bpy.context.scene
    target_object = bpy.data.objects.get(object_name)
    if not target_object:
        raise ValueError(f"Object named '{object_name}' not found!")
    
    # --- World Node & HDRI Pre-loading ---
    settings = scene.lora_render_settings
    hdri_folder = bpy.path.abspath(settings.hdri_folder)
    override_world = settings.override_world
    
    hdri_files = [] 

    if hdri_folder and os.path.exists(hdri_folder) and (override_world or not scene.world):
        if not scene.world:
            scene.world = bpy.data.worlds.new("AngleCraft_World")
        scene.world.use_nodes = True
        nodes = scene.world.node_tree.nodes
        links = scene.world.node_tree.links

        env_node = next((node for node in nodes if node.type == 'TEX_ENVIRONMENT'), None)
        if not env_node:
            env_node = nodes.new(type="ShaderNodeTexEnvironment")
            bg_node = next((node for node in nodes if node.type == 'BACKGROUND'), None)
            if bg_node:
                links.new(env_node.outputs['Color'], bg_node.inputs['Color'])

        # PRE-LOAD Images to memory
        hdri_files = [f for f in os.listdir(hdri_folder) if f.lower().endswith(('.hdr', '.exr'))]
        for f in hdri_files:
            img_path = os.path.join(hdri_folder, f)
            if not bpy.data.images.get(f):
                bpy.data.images.load(img_path)

    # 1. Get Points
    if distribution_type == "fibonacci":
        points = fibonacci_sphere(samples=num_cameras_horizontal * num_cameras_vertical, radius=1.0, half_sphere=half_sphere, seed=seed)
    elif distribution_type == "linear":
        points = linear_distribution(num_cameras_horizontal, num_cameras_vertical, radius=1.0, half_sphere=half_sphere)
    elif distribution_type == "uniform":
        points = uniform_distribution(num_cameras_horizontal, num_cameras_vertical, radius=1.0, half_sphere=half_sphere)
    elif distribution_type == "equator_dense":
        points = equator_dense_distribution(num_cameras_horizontal, num_cameras_vertical, radius=1.0, half_sphere=half_sphere)
    elif distribution_type == "weighted":
        points = weighted_distribution(num_cameras_horizontal * num_cameras_vertical, bias_ratio=0.8)
    elif distribution_type == "ai_blueprint":  # --- NEW: Hook into the distribution type ---
        points = ai_blueprint_distribution(radius=1.0, half_sphere=half_sphere)

    if remove_overlapping:
        points = remove_overlapping_cameras(points, overlap_threshold)

    # 2. Setup the Single Master Camera
    cam_name = f"{target_object.name}_AngleCraft_Cam"
    master_camera = bpy.data.objects.get(cam_name)

    if not master_camera:
        bpy.ops.object.camera_add()
        master_camera = bpy.context.object
        master_camera.name = cam_name

    master_camera.animation_data_clear()

    # --- Setup Preview Empties Collection ---
    preview_col_name = "AngleCraft_Preview"
    preview_col = bpy.data.collections.get(preview_col_name)
    if preview_col:
        # Wrap in list() to safely delete while iterating
        for obj in list(preview_col.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
    else:
        preview_col = bpy.data.collections.new(preview_col_name)
        scene.collection.children.link(preview_col)

    preview_col.hide_viewport = False

    # --- Prep Floor for Keyframing ---
    floor_name = scene.lora_object_settings.floor_object_name
    floor_object = bpy.data.objects.get(floor_name) if floor_name != 'NONE' else None
    
    floor_z_max = 0
    if floor_object:
        floor_object.animation_data_clear() 
        floor_z_max = max((floor_object.matrix_world @ Vector(corner)).z for corner in floor_object.bound_box)

    # 3. Setup Timeline constraints
    total_frames = len(points)
    scene.frame_start = 1
    scene.frame_end = total_frames
    random.seed(seed)

    # 4. Insert Keyframes & Build Preview
    for idx, point in enumerate(points):
        frame = idx + 1 
        radius = random.uniform(min_radius, max_radius)
        camera_location = target_object.location + Vector(point) * radius

        master_camera.location = camera_location
        direction = target_object.location - master_camera.location
        master_camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

        master_camera.keyframe_insert(data_path="location", frame=frame)
        master_camera.keyframe_insert(data_path="rotation_euler", frame=frame)

        # Generate Preview Empty
        empty = bpy.data.objects.new(f"AC_Preview_{idx:03d}", None)
        empty.empty_display_type = 'SPHERE' 
        empty.empty_display_size = 0.15 
        empty.location = camera_location
        empty.rotation_euler = master_camera.rotation_euler
        preview_col.objects.link(empty)

        # Floor hiding
        if floor_object:
            is_below_floor = camera_location.z < floor_z_max
            floor_object.hide_render = is_below_floor
            floor_object.hide_viewport = is_below_floor
            floor_object.keyframe_insert(data_path="hide_render", frame=frame)
            floor_object.keyframe_insert(data_path="hide_viewport", frame=frame)

    # --- BLENDER 5.0 SLOTTED ACTION FIX ---
    if floor_object and floor_object.animation_data and floor_object.animation_data.action:
        anim_data = floor_object.animation_data
        fcurves = []
        
        if hasattr(anim_data, "action_slot") and anim_data.action_slot:
            from bpy_extras import anim_utils
            channelbag = anim_utils.action_get_channelbag_for_slot(anim_data.action, anim_data.action_slot)
            if channelbag:
                fcurves = channelbag.fcurves
        elif hasattr(anim_data.action, "fcurves"):
            fcurves = anim_data.action.fcurves

        for fcurve in fcurves:
            if fcurve.data_path in ("hide_render", "hide_viewport"):
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'CONSTANT'

    return master_camera, total_frames


def delete_ai_cameras():
    """
    Deletes the master animated camera and the preview collection.
    """
    # Wrap in list() to prevent skipping cameras if multiple exist
    cameras_to_delete = [camera for camera in bpy.data.objects if camera.type == 'CAMERA' and 'AngleCraft_Cam' in camera.name]
    for camera in cameras_to_delete:
        bpy.data.objects.remove(camera, do_unlink=True)

    preview_col = bpy.data.collections.get("AngleCraft_Preview")
    if preview_col:
        # Wrap in list() to safely delete all preview empties
        for obj in list(preview_col.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
            
        for scene in bpy.data.scenes:
            if preview_col.name in scene.collection.children:
                scene.collection.children.unlink(preview_col)
        bpy.data.collections.remove(preview_col)


# -------------------------------------------------------------------
# OPERATOR CLASSES
# -------------------------------------------------------------------
class AngleCraftCreateCamerasOperator(bpy.types.Operator):
    bl_idname = "object.create_lora_cameras"
    bl_label = "Create Camera Animation"
    
    def execute(self, context):
        scene = context.scene
        try:
            master_cam, total_frames = create_cameras(
                object_name=scene.lora_object_settings.object_name,
                min_radius=scene.lora_camera_sphere_settings.min_radius,
                max_radius=scene.lora_camera_sphere_settings.max_radius,
                num_cameras_horizontal=scene.lora_camera_sphere_settings.num_cameras_horizontal,
                num_cameras_vertical=scene.lora_camera_sphere_settings.num_cameras_vertical,
                distribution_type=scene.lora_camera_sphere_settings.sphere_type,
                half_sphere=scene.lora_camera_sphere_settings.half_sphere,
                remove_overlapping=scene.lora_camera_sphere_settings.remove_overlapping,
                overlap_threshold=scene.lora_camera_sphere_settings.overlap_threshold,
                seed=scene.lora_camera_sphere_settings.random_seed
            )
            scene.lora_render_button_settings.info_num_cameras = total_frames        
            return {'FINISHED'}
        except ValueError as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

class AngleCraftDeleteCamerasOperator(bpy.types.Operator):
    bl_idname = "object.delete_lora_cameras"
    bl_label = "Delete Camera Animation"
    
    def execute(self, context):
        delete_ai_cameras()
        context.scene.lora_render_button_settings.info_num_cameras = 0   
        return {'FINISHED'}