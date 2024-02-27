# 把csv中的position与rotation转变为blender中的position与rotation，以csv表头的名字对应为blender中objects的名字
import numpy as np
import bpy
import csv

# read csv file
csv_path = "/home/chen/Desktop/code/CALM/state_timestamp.csv"
armature_npy_path = "/home/chen/Desktop/code/CALM/armature.npy"
csv_file = open(csv_path, "r")
reader = csv.reader(csv_file)
# get the header
# header = next(reader)
# get the data
data = []
for row in reader:
    data.append(row)
# close csv file
csv_file.close()

# # header 删去frame
# header = header[1:]
# # data 删去frame
# for i in range(len(data)):
#     data[i] = data[i][1:]

# read armature.npy
armature = np.load(armature_npy_path, allow_pickle=True).item()

# get joint name
joint_name = armature["joint_names"]
# get joint number
joint_num = len(joint_name)

# get root joint pos rot and non root joint rot
root_pos = data[:, :3]
root_rot = data[:, 3:7]
non_root_rot = data[:, 7:].reshape(-1, joint_num - 1, 4)

# set keyframe
# get armature object
armature_obj = bpy.data.objects["Armature"]

# set root joint pos rot
for i in range(len(root_pos)):
    # set root joint pos
    armature_obj.location = root_pos[i]
    # set root joint rot
    armature_obj.rotation_mode = "QUATERNION"
    armature_obj.rotation_quaternion = root_rot[i]
    # set keyframe
    armature_obj.keyframe_insert(data_path="location", frame=i)
    armature_obj.keyframe_insert(data_path="rotation_quaternion", frame=i)

# set non root joint rot
for i in range(len(non_root_rot)):
    for j in range(joint_num - 1):
        # set non root joint rot
        joint_obj = bpy.data.objects[joint_name[j]]
        joint_obj.rotation_mode = "QUATERNION"
        joint_obj.rotation_quaternion = non_root_rot[i][j]
        # set keyframe
        joint_obj.keyframe_insert(data_path="rotation_quaternion", frame=i)
