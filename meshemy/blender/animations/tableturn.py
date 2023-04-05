import bpy


def add_table_turn_animation(number_of_frames: int = 250) -> None:
    # Set the timeline duration
    start_frame = 1
    end_frame = number_of_frames

    # Set the rotation axis (Z-axis in this case)
    axis = (0, 0, 1)

    # Clear any existing animation data
    obj = bpy.context.active_object
    obj.animation_data_clear()

    # Create a new action and assign it to the object
    action = bpy.data.actions.new(name="TableTurn")
    obj.animation_data_create()
    obj.animation_data.action = action

    # Set keyframes for the start and end of the rotation
    bpy.context.scene.frame_set(start_frame)
    obj.rotation_euler = (0, 0, 0)
    obj.keyframe_insert(data_path="rotation_euler", frame=start_frame)

    bpy.context.scene.frame_set(end_frame)
    obj.rotation_euler = (0, 0, 6.28319)  # 2 * pi radians (360 degrees)
    obj.keyframe_insert(data_path="rotation_euler", frame=end_frame)

    # Set the end frame for the timeline
    bpy.context.scene.frame_end = end_frame
