from isaacgym.torch_utils import *
import sys
sys.path.append(r"/home/chen/Desktop/code/CALM/calm/utils")
import torch_utils
import torch

# 创建一个四元数tensor
quat = torch.tensor([0.462, 0.191, 0.462, 0.733], dtype=torch.float32)
# 修改shape为（1，4）
quat = quat.unsqueeze(0)
heading_rot = torch_utils.calc_heading_quat_inv(quat)