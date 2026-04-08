import bpy

# Properties to control object settings
class AngleCraftObjectSettings(bpy.types.PropertyGroup):
    def update_object_list(self, context):
        self["object_name"] = self.object_name

    def update_floor_list(self, context):
        self["floor_object_name"] = self.floor_object_name

    def object_enum_items(self, context):
        return [(obj.name, obj.name, "") for obj in bpy.data.objects if obj.type == 'EMPTY']

    def floor_enum_items(self, context):
        items = [(obj.name, obj.name, "") for obj in bpy.data.objects if obj.type == 'MESH']
        items.insert(0, ('NONE', 'None', 'No object selected'))
        return items

    object_name: bpy.props.EnumProperty(
        name="Camera target",
        description="Select the target empty for camera placement",
        items=object_enum_items,
        update=update_object_list
    )
    
    floor_object_name: bpy.props.EnumProperty(
        name="Floor Mesh",
        description="Select the floor mesh object",
        items=floor_enum_items,
        update=update_floor_list
    )

# Properties to control camera sphere settings
class AngleCraftCameraSphereSettings(bpy.types.PropertyGroup):
    min_radius: bpy.props.FloatProperty(name="Min Radius", default=10.0, min=0.1)
    max_radius: bpy.props.FloatProperty(name="Max Radius", default=10.0, min=0.1)
    radius: bpy.props.FloatProperty(name="Radius", default=10.0, min=0.1)
    
    num_cameras_horizontal: bpy.props.IntProperty(name="Horizontal Cameras", default=16, min=1)
    num_cameras_vertical: bpy.props.IntProperty(name="Vertical Cameras", default=8, min=1)
    
    half_sphere: bpy.props.BoolProperty(name="Half Sphere", default=False)
    
    # AI Blueprint Toggles
    blueprint_cardinals: bpy.props.BoolProperty(name="Cardinals (Front, Back, L, R)", default=True)
    blueprint_isometrics: bpy.props.BoolProperty(name="Isometrics (3/4 Views)", default=True)
    blueprint_top_bottom: bpy.props.BoolProperty(name="Top / Bottom", default=True)
    
    sphere_type: bpy.props.EnumProperty(
        name="Sphere Type",
        items=[
            ('linear', 'Linear', 'Linear distribution of cameras'),
            ('uniform', 'Uniform', 'Uniform distribution of cameras'),
            ('fibonacci', 'Fibonacci', 'Fibonacci sphere distribution'),
            ('equator_dense', 'Equator Dense', 'Denser distribution of cameras at the equator'),
            ('weighted', 'Weighted (Top 80%, Bottom 20%)', '80% cameras on top, 20% on bottom'),
            ('ai_blueprint', 'AI Blueprint (Vizcom/Gemini)', 'Ideal configurable views for AI'),
        ],
        default='ai_blueprint'
    )

    remove_overlapping: bpy.props.BoolProperty(name="Remove Overlapping", default=False)
    overlap_threshold: bpy.props.FloatProperty(name="Overlap Threshold", default=0.1, min=0.0)
    random_seed: bpy.props.IntProperty(name="Random Seed", default=42)

# Properties for HDRI environment settings
class AngleCraftRenderSettings(bpy.types.PropertyGroup):
    hdri_folder: bpy.props.StringProperty(
        name="HDRI Folder",
        default="",
        subtype='DIR_PATH'
    )
    override_world: bpy.props.BoolProperty(name="Override World", default=False)
    frames_per_hdri: bpy.props.IntProperty(name="Frames per HDRI", default=1, min=1)

# Properties for internal UI state
class AngleCraftRenderButtonSettings(bpy.types.PropertyGroup):
    info_num_cameras: bpy.props.IntProperty(
        name="Number of Cameras",
        default=0,
        options={'HIDDEN'}
    )