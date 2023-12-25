# generate armature and bones from npy file

import bpy
import numpy as np
import os

# load npy file
sk_filepath = "/home/chen/Desktop/code/CALM/calm/poselib/armature.npy"
sk_dict = np.load(sk_filepath, allow_pickle=True).item()

node_names = sk_dict["joint_names"]
parent_indices = sk_dict["parent_indices"]
local_translation = sk_dict["joint_local_translation"]

num_joint = len(node_names)


global_translation = np.zeros((num_joint, 3))
for i in range(num_joint):
    if parent_indices[i] == -1:
        global_translation[i] = local_translation[i]
    else:
        global_translation[i] = global_translation[parent_indices[i]] + local_translation[i]



# move the armature to the ground
# foot_height = 0.05
# global_translation[:, 2] -= foot_height

# create armature
armature_name = "Armature"
armature = bpy.data.armatures.new(armature_name)
armature_obj = bpy.data.objects.new(armature_name, armature)
bpy.context.scene.collection.objects.link(armature_obj)

# create bones
bpy.context.view_layer.objects.active = armature_obj
armature_obj.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')

for i in range(num_joint):
    if node_names[i] == "none":
        continue
    bone = armature.edit_bones.new(node_names[i])
    bone.head = (0, 0, 0) if parent_indices[i] == -1 else global_translation[parent_indices[i]]
    bone.tail = global_translation[i]
    if parent_indices[i] != -1:
        bone.parent = armature.edit_bones[node_names[parent_indices[i]]]

bpy.ops.object.mode_set(mode='OBJECT')

# paint weights

