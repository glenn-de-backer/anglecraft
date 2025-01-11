import bpy
import math
from mathutils import Vector
import os
import re
import random  

def generate_sphere_points(num_horizontal, num_vertical, radius, hemisphere=None):
    """
    Generate points on the surface of a sphere using spherical coordinates.
    
    Args:
        num_horizontal (int): The number of points to be placed horizontally.
        num_vertical (int): The number of points to be placed vertically.
        radius (float): The radius of the sphere.
        hemisphere (str): If 'top', only generates points in the upper hemisphere.
                          If 'bottom', only generates points in the lower hemisphere.
    
    Returns:
        List[tuple]: A list of 3D coordinates representing points on the sphere.
    """
    points = []

    # Ensure we do not divide by zero and there are points to generate
    if num_horizontal <= 0 or num_vertical <= 0:
        return points

    for i in range(num_vertical):
        if hemisphere == 'top':
            vertical_angle = (math.pi / 2) * (i / (num_vertical - 1))  # Scale between 0 and π/2
        elif hemisphere == 'bottom':
            vertical_angle = (math.pi / 2) * (i / (num_vertical - 1)) + math.pi / 2  # Scale between π/2 and π
        else:
            vertical_angle = math.pi * i / (num_vertical - 1)  # Scale between 0 and π
        
        for j in range(num_horizontal):
            horizontal_angle = 2 * math.pi * j / num_horizontal  # Scale between 0 and 2π
            x = radius * math.sin(vertical_angle) * math.cos(horizontal_angle)
            y = radius * math.sin(vertical_angle) * math.sin(horizontal_angle)
            z = radius * math.cos(vertical_angle)
            points.append((x, y, z))
    
    return points

def weighted_distribution(num_cameras_total, bias_ratio=0.8):
    """
    Generate points on a sphere with a weighted distribution.
    
    Args:
        num_cameras_total (int): The total number of cameras to be placed.
        bias_ratio (float): Ratio of points in the top hemisphere (0.8 by default).
    
    Returns:
        List[tuple]: A list of 3D coordinates for the camera positions.
    """
    # Calculate the number of cameras for the top and bottom hemispheres
    top_cameras = int(num_cameras_total * bias_ratio)
    bottom_cameras = num_cameras_total - top_cameras

    # Calculate the number of horizontal and vertical divisions for each hemisphere
    num_horizontal_top = int(math.ceil(math.sqrt(top_cameras)))
    num_vertical_top = int(math.ceil(top_cameras / num_horizontal_top))
    
    num_horizontal_bottom = int(math.ceil(math.sqrt(bottom_cameras)))
    num_vertical_bottom = int(math.ceil(bottom_cameras / num_horizontal_bottom))

    # Generate points for the top hemisphere
    top_sphere_points = generate_sphere_points(num_horizontal_top, num_vertical_top, radius=1.0, hemisphere='top')

    # Generate points for the bottom hemisphere
    bottom_sphere_points = generate_sphere_points(num_horizontal_bottom, num_vertical_bottom, radius=1.0, hemisphere='bottom')

    # Limit the points to the exact number needed
    top_sphere_points = top_sphere_points[:top_cameras]
    bottom_sphere_points = bottom_sphere_points[:bottom_cameras]

    return top_sphere_points + bottom_sphere_points


def fibonacci_sphere(samples=1, radius=1.0, half_sphere=False):
    """
    Generate points on the surface of a sphere using the Fibonacci sphere method.
    
    Args:
        samples (int): The number of points to generate.
        radius (float): The radius of the sphere.
        half_sphere (bool): If True, only generates points in the upper hemisphere.
    
    Returns:
        List[tuple]: A list of 3D coordinates representing points on the sphere.
    """
    points = []
    phi = math.pi * (3. - math.sqrt(5.))  # Golden angle in radians

    for i in range(samples):
        z = 1 - (i / float(samples - 1)) * 2  # z goes from 1 to -1
        if half_sphere and z < 0:
            continue  # Skip points below the equator if using half-sphere
        radius_z = math.sqrt(1 - z * z)  # radius at z

        theta = phi * i  # Golden angle increment

        x = math.cos(theta) * radius_z
        y = math.sin(theta) * radius_z

        points.append((x * radius, y * radius, z * radius))

    return points


def linear_distribution(num_cameras_horizontal, num_cameras_vertical, radius, half_sphere=False):
    """
    Generate points distributed in a linear grid on the surface of a sphere.
    
    Args:
        num_cameras_horizontal (int): The number of cameras to be placed horizontally.
        num_cameras_vertical (int): The number of cameras to be placed vertically.
        radius (float): The radius of the sphere.
        half_sphere (bool): If True, only generates points in the upper hemisphere.
    
    Returns:
        List[tuple]: A list of 3D coordinates for the camera positions.
    """
    points = []
    for v in range(num_cameras_vertical):
        if half_sphere:
            vertical_angle = (math.pi / 2) * (v / (num_cameras_vertical - 1))  # Scale between 0 and π/2
        else:
            vertical_angle = math.pi * (v + 1) / (num_cameras_vertical + 1)  # Scale between 0 and π

        for h in range(num_cameras_horizontal):
            horizontal_angle = (2 * math.pi / num_cameras_horizontal) * h
            x = radius * math.sin(vertical_angle) * math.cos(horizontal_angle)
            y = radius * math.sin(vertical_angle) * math.sin(horizontal_angle)
            z = radius * math.cos(vertical_angle)
            points.append((x, y, z))
    return points


def uniform_distribution(num_cameras_horizontal, num_cameras_vertical, radius, half_sphere=False):
    """
    Generate points uniformly distributed on the surface of a sphere.
    
    Args:
        num_cameras_horizontal (int): The number of cameras to be placed horizontally.
        num_cameras_vertical (int): The number of cameras to be placed vertically.
        radius (float): The radius of the sphere.
        half_sphere (bool): If True, only generates points in the upper hemisphere.
    
    Returns:
        List[tuple]: A list of 3D coordinates for the camera positions.
    """
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
    """
    Generate points with higher density near the equator on the surface of a sphere.
    
    Args:
        num_cameras_horizontal (int): The number of cameras to be placed horizontally.
        num_cameras_vertical (int): The number of cameras to be placed vertically.
        radius (float): The radius of the sphere.
        half_sphere (bool): If True, only generates points in the upper hemisphere.
    
    Returns:
        List[tuple]: A list of 3D coordinates for the camera positions.
    """
    points = []
    for v in range(num_cameras_vertical):
        # Adjust the vertical angle to create a higher density at the equator
        t = (v + 0.5) / num_cameras_vertical  # Normalize v to range [0, 1]
        if half_sphere:
            vertical_angle = math.asin(t) * (math.pi / 2)  # Scale to [0, π/2] for half sphere
        else:
            vertical_angle = math.asin(2 * t - 1) + (math.pi / 2)  # Scale to [0, π] for full sphere

        for h in range(num_cameras_horizontal):
            horizontal_angle = (2 * math.pi / num_cameras_horizontal) * h
            x = radius * math.sin(vertical_angle) * math.cos(horizontal_angle)
            y = radius * math.sin(vertical_angle) * math.sin(horizontal_angle)
            z = radius * math.cos(vertical_angle)
            points.append((x, y, z))
    return points

def remove_overlapping_cameras(points, threshold):
    """
    Remove overlapping cameras by filtering out points that are too close to each other.
    
    Args:
        points (List[tuple]): A list of 3D coordinates representing points on the sphere.
        threshold (float): The minimum distance between cameras to avoid overlap.
    
    Returns:
        List[Vector]: A list of 3D coordinates with overlapping points removed.
    """    
    filtered_points = []
    for point in points:
        # Convert point to Vector
        point_vec = Vector(point)
        if all((point_vec - Vector(other)).length >= threshold for other in filtered_points):
            filtered_points.append(point_vec)
    return filtered_points

def create_cameras(object_name, min_radius, max_radius, num_cameras_horizontal, num_cameras_vertical, distribution_type="fibonacci", half_sphere=False, camera_base=None, remove_overlapping=False, overlap_threshold=0.1):
    """
    Create cameras in a spherical arrangement around a target object.
    
    This function generates points on a sphere based on the specified distribution type,
    places cameras at those points, and optionally removes overlapping cameras.
    
    Args:
        object_name (str): The name of the target object.
        min_radius (float): The minimum distance of cameras from the object.
        max_radius (float): The maximum distance of cameras from the object.
        num_cameras_horizontal (int): The number of cameras in the horizontal circle.
        num_cameras_vertical (int): The number of vertical levels of cameras.
        distribution_type (str): The type of sphere generation ('fibonacci', 'linear', 'uniform', 'equator_dense', 'weighted').
        half_sphere (bool): If True, create only the upper half of the cameras.
        camera_base (str): The name of the base camera to clone, or None to create new cameras.
        remove_overlapping (bool): If True, remove overlapping cameras.
        overlap_threshold (float): The minimum distance between cameras to avoid overlap.
    
    Returns:
        List[bpy.types.Object]: A list of created camera objects.
    
    Raises:
        ValueError: If the target object is not found or an unknown distribution type is specified.
    """
    target_object = bpy.data.objects.get(object_name)
    if not target_object:
        raise ValueError(f"Object named '{object_name}' not found!")
    
    base_camera = bpy.data.objects.get(camera_base) if camera_base and camera_base != "None" else None

    if distribution_type == "fibonacci":
        points = fibonacci_sphere(samples=num_cameras_horizontal * num_cameras_vertical, radius=1.0, half_sphere=half_sphere)
    elif distribution_type == "linear":
        points = linear_distribution(num_cameras_horizontal, num_cameras_vertical, radius=1.0, half_sphere=half_sphere)
    elif distribution_type == "uniform":
        points = uniform_distribution(num_cameras_horizontal, num_cameras_vertical, radius=1.0, half_sphere=half_sphere)
    elif distribution_type == "equator_dense":
        points = equator_dense_distribution(num_cameras_horizontal, num_cameras_vertical, radius=1.0, half_sphere=half_sphere)
    elif distribution_type == "weighted":
        points = weighted_distribution(num_cameras_horizontal * num_cameras_vertical, bias_ratio=0.8)
    else:
        raise ValueError(f"Unknown distribution type: {distribution_type}")

    if remove_overlapping:
        points = remove_overlapping_cameras(points, overlap_threshold)

    cameras = []
    for idx, point in enumerate(points):
        radius = random.uniform(min_radius, max_radius)
        camera_location = target_object.location + Vector(point) * radius

        if base_camera:
            new_camera = base_camera.copy()
            new_camera.data = base_camera.data.copy()
            new_camera.location = camera_location
            bpy.context.collection.objects.link(new_camera)
        else:
            bpy.ops.object.camera_add(location=camera_location)
            new_camera = bpy.context.object

        direction = target_object.location - new_camera.location
        new_camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

        new_camera.name = f"{target_object.name}_ai_{idx}"
        cameras.append(new_camera)

    print(f"Created {len(cameras)} cameras around '{object_name}'.")
    return cameras


def render_cameras(output_directory, render_samples, denoise_enabled, denoiser, render_resolution, hdri_folder, override_world):
    """
    Render images from all cameras with the '_ai' suffix and save them to the output directory.
    
    Args:
        output_directory (str): The directory to save rendered images.
        render_samples (int): The number of render samples.
        denoise_enabled (bool): Whether denoising should be enabled.
        denoiser (str): The denoiser to use for rendering.
        render_resolution (tuple): The resolution of the rendered images (width, height).
        hdri_folder (str): The folder containing HDRi images for lighting.
        override_world (bool): Whether to override the world settings with an HDRi.
    
    Returns:
        None
    """
    # Convert the output directory to an absolute path
    output_directory = bpy.path.abspath(output_directory)

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Convert the HDRi folder path to an absolute path
    hdri_folder = bpy.path.abspath(hdri_folder)

    # Get a list of HDRi files (with extensions .hdr or .exr) from the specified folder
    hdri_files = [os.path.join(hdri_folder, f) for f in os.listdir(hdri_folder) if f.lower().endswith(('.hdr', '.exr'))] if os.path.isdir(hdri_folder) else []

    # Select cameras with names containing the '_ai' suffix
    cameras_to_render = [camera for camera in bpy.data.objects if camera.type == 'CAMERA' and re.search(r'_ai_\d+', camera.name)]

    # Access the current scene in Blender
    scene = bpy.context.scene

    # Set the render engine to Cycles and configure the render settings
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = render_samples  # Set the number of samples for rendering
    scene.render.resolution_x, scene.render.resolution_y = render_resolution  # Set the resolution for rendering

    # Set color management to Filmic with High Contrast look
    scene.view_settings.view_transform = 'Filmic'
    scene.view_settings.look = 'High Contrast'

    # Set the image format to PNG
    scene.render.image_settings.file_format = 'PNG'

    # Enable or disable denoising based on the 'denoise_enabled' flag
    if denoise_enabled:
        scene.cycles.use_denoising = True
        scene.cycles.denoiser = denoiser  # Set the specific denoiser (e.g., OptiX, NLM)
    else:
        scene.cycles.use_denoising = False

    # Retrieve the floor object (if any) to hide it during rendering if necessary
    floor_object_name = scene.lora_object_settings.floor_object_name
    floor_object = bpy.data.objects.get(floor_object_name) if floor_object_name else None

    # Initialize the progress bar
    wm = bpy.context.window_manager
    total_steps = len(cameras_to_render)
    wm.progress_begin(0, total_steps)

    # Iterate through each camera that was selected for rendering
    for i, camera in enumerate(cameras_to_render):
        scene.camera = camera  # Set the current camera for rendering

        # If HDRi images are available and the world needs to be overridden or there is no existing world,
        # set the world environment texture to a random HDRi image
        if hdri_files and (override_world or not scene.world):
            random_hdri = random.choice(hdri_files)  # Pick a random HDRi image
            if not scene.world:
                scene.world = bpy.data.worlds.new("World")  # Create a new world if none exists
            scene.world.use_nodes = True  # Enable nodes for the world settings
            nodes = scene.world.node_tree.nodes
            links = scene.world.node_tree.links

            # Look for the "Environment Texture" node, if it doesn't exist, create one
            env_node = nodes.get("Environment Texture")
            if not env_node:
                env_node = nodes.new(type="ShaderNodeTexEnvironment")
                links.new(env_node.outputs[0], nodes["Background"].inputs[0])  # Link the node to the background shader

            env_node.image = bpy.data.images.load(random_hdri)  # Set the environment texture to the selected HDRi

        # If a floor object is specified and the camera is below the floor object, hide the floor during rendering
        if floor_object:
            camera_below_floor = camera.location.z < floor_object.location.z
            if camera_below_floor:
                floor_object.hide_render = True  # Hide the floor object during rendering

        # Set the file path where the rendered image will be saved
        filepath = os.path.join(output_directory, f"render_{i:03d}.png")
        scene.render.filepath = filepath  # Set the render output path

        # Perform the render and save the image
        bpy.ops.render.render(write_still=True)

        # If the floor object was hidden earlier, restore its visibility for subsequent renders
        if floor_object:
            floor_object.hide_render = False  # Restore render visibility

        # Update the progress bar
        wm.progress_update(i + 1)

    # End the progress bar
    wm.progress_end()

    # Print a message indicating how many images were rendered
    print(f"Rendered {len(cameras_to_render)} images to {output_directory}.")



def delete_ai_cameras():
    """
    Delete all cameras with the '_ai' suffix from the scene.
    
    Returns:
        None
    """
    cameras_to_delete = [camera for camera in bpy.data.objects if camera.type == 'CAMERA' and re.search(r'_ai_\d+', camera.name)]

    for camera in cameras_to_delete:
        bpy.data.objects.remove(camera, do_unlink=True)

    print(f"Deleted {len(cameras_to_delete)} cameras with the '_ai' suffix.")


# Operator to create cameras
class AngleCraftCreateCamerasOperator(bpy.types.Operator):
    """
    Operator to create cameras in a spherical arrangement around a target object.

    This operator gathers the settings from the scene properties and creates cameras
    based on the user-defined parameters such as number of horizontal/vertical cameras,
    radius, and sphere distribution type.
    """
    bl_idname = "object.create_lora_cameras"
    bl_label = "Create Camera sphere"
    
    def execute(self, context):
        """
        Executes the camera creation process based on the provided settings.

        Args:
            context: The current Blender context, including scene and other settings.
        
        Returns:
            {'FINISHED'}: Indicates the operation completed successfully.
        """
        # Gather settings from the scene
        object_name = context.scene.lora_object_settings.object_name
        min_radius = context.scene.lora_camera_sphere_settings.min_radius
        max_radius = context.scene.lora_camera_sphere_settings.max_radius
        num_cameras_horizontal = context.scene.lora_camera_sphere_settings.num_cameras_horizontal
        num_cameras_vertical = context.scene.lora_camera_sphere_settings.num_cameras_vertical
        distribution_type = context.scene.lora_camera_sphere_settings.sphere_type
        half_sphere = context.scene.lora_camera_sphere_settings.half_sphere
        camera_base = context.scene.lora_camera_settings.camera_base
        remove_overlapping = context.scene.lora_camera_sphere_settings.remove_overlapping
        overlap_threshold = context.scene.lora_camera_sphere_settings.overlap_threshold

        # Create cameras around the object
        cameras = create_cameras(
            object_name=object_name,
            min_radius=min_radius,
            max_radius=max_radius,
            num_cameras_horizontal=num_cameras_horizontal,
            num_cameras_vertical=num_cameras_vertical,
            distribution_type=distribution_type,
            half_sphere=half_sphere,
            camera_base=camera_base,
            remove_overlapping=remove_overlapping,
            overlap_threshold=overlap_threshold
        )

        # Update number of cameras
        context.scene.lora_render_button_settings.info_num_cameras = len(cameras)        

        return {'FINISHED'}
    
# Operator to render from the created cameras
class AngleCraftRenderCamerasOperator(bpy.types.Operator):
    """
    Operator to render images from the cameras created around an object.

    This operator accesses the render settings and triggers the rendering process 
    based on the user-defined settings such as render resolution, samples, denoising, etc.
    """
    bl_idname = "object.render_lora_cameras"
    bl_label = "Render all cameras in sphere"
    
    def execute(self, context):
        """
        Executes the rendering process using the defined render settings.

        Args:
            context: The current Blender context, including scene and other settings.

        Returns:
            {'FINISHED'}: Indicates the operation completed successfully.
        """
        # Access render settings from the correct property group
        render_settings = context.scene.lora_render_settings

        
        render_cameras(
            output_directory=render_settings.output_directory,
            render_samples=render_settings.render_samples,
            denoise_enabled=render_settings.denoise_enabled,
            denoiser=render_settings.denoiser,
            render_resolution=render_settings.render_resolution,
            hdri_folder=render_settings.hdri_folder,  # Pass the HDRI folder setting
            override_world=render_settings.override_world
        )

        # Notify the user that rendering is complete
        self.report({'INFO'}, "Rendering complete. Check the output directory for images.")
                
        return {'FINISHED'}

# Operator to delete cameras
class AngleCraftDeleteCamerasOperator(bpy.types.Operator):
    """
    Operator to delete all cameras that were created in the scene.

    This operator is used to clean up the scene by removing cameras that were
    previously placed based on the settings.
    """
    bl_idname = "object.delete_lora_cameras"
    bl_label = "Delete Camera sphere"
    
    def execute(self, context):
        """
        Executes the camera deletion process.

        Args:
            context: The current Blender context.

        Returns:
            {'FINISHED'}: Indicates the operation completed successfully.
        """
        delete_ai_cameras()

        # update number of cameras
        context.scene.lora_render_button_settings.info_num_cameras = 0   
 
        return {'FINISHED'}