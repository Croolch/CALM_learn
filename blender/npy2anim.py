# 将npy文件转为blender动画

# import bpy
import numpy as np

# load npy file
npy_filepath = "/home/chen/Desktop/code/CALM/calm/poselib/mydata/RL_Avatar_WalkRight02_Motion.npy"
npy_dict = np.load(npy_filepath, allow_pickle=True).item()

print(npy_dict.keys())