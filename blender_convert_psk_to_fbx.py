import bpy
import sys


PSK_PATH = sys.argv[4]
FBX_PATH = sys.argv[5]


def set_world_units_and_apply(psk_path, fbx_path):
    '''
    Sets the scene to Meters, scales the armature up by 100 and applies that to the armature and meshes.
    Also removes the starter camera, cube and light.
    '''
    progress_value = 0

    bpy.ops.import_scene.psk(filepath=psk_path)

    # Create a list for armatures and meshes
    armatures = [obj for obj in bpy.context.scene.objects if obj.type == "ARMATURE"]
    meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]

    total_objects = len([obj for obj in bpy.context.scene.objects if obj.type == "MESH" or obj.type == "ARMATURE"]) + 1
    print("~PROGRESSBAR~ set_length: %s" % total_objects)

    # Set Scene units
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 0.01
    bpy.context.scene.unit_settings.length_unit = "METERS"
    
    # Scale the rig by 100 units.
    if armatures:
        for armature in armatures:
            print("ARMATURE =", armature)
            armature.scale[0] = 100
            armature.scale[1] = 100
            armature.scale[2] = 100
            bpy.ops.object.transform_apply({"selected_editable_objects": armatures}, location=True, rotation=True, scale=True)
            progress_value += 1
            print("~PROGRESSBAR~ set_value: %s" % (progress_value))
    
    for mesh in meshes:
        if not armatures:
            mesh.scale[0] = 100
            mesh.scale[1] = 100
            mesh.scale[2] = 100
        print("MESH =", mesh)
        bpy.ops.object.transform_apply({"selected_editable_objects": meshes}, location=True, rotation=True, scale=True)
        progress_value += 1
        print("~PROGRESSBAR~ set_value: %s" % (progress_value))

    # Delete default meshe/light/camera
    objs = [bpy.context.scene.objects["Camera"], bpy.context.scene.objects["Cube"], bpy.context.scene.objects["Light"]]
    bpy.ops.object.delete({"selected_objects": objs})
    
    bpy.ops.export_scene.fbx(filepath=fbx_path,
                             use_selection=False,
                             use_active_collection=False,
                             object_types={"EMPTY", "CAMERA", "LIGHT", "ARMATURE", "MESH", "OTHER"},
                             global_scale=1.00,
                             apply_scale_options="FBX_SCALE_NONE",
                             apply_unit_scale=True,
                             mesh_smooth_type="EDGE",
                             use_mesh_modifiers=True,
                             add_leaf_bones=False,
                             bake_anim=False,
                             use_subsurf=False,
                             use_mesh_edges=False,
                             use_tspace=False)
    print("~PROGRESSBAR~ set_value: %s" % (progress_value + 1))
    

set_world_units_and_apply(PSK_PATH, FBX_PATH)