import os
import numpy as np
import csv
import time

from isaacgym.torch_utils import *

from . import torch_utils


def save_to_csv(frame, root_state, dof_pos, dof_offset):
    # frame: Tensor, shape: (1)
    # root_state: Tensor, shape: (13,)
    # dof_pos: Tensor, shape: (31,)
    # dof_offset: List, shape: (14,)

    assert dof_offset[-1] == len(dof_pos)
    # prepare frame
    # frame = frame.cpu().numpy()

    # prepare root state
    root_pos_and_rot = root_state[:7]

    # process non root state
    non_root_joint_rot = []
    for i in range(len(dof_offset) - 1):
        dof_start = dof_offset[i]
        dof_size = dof_offset[i + 1] - dof_start
        joint_pose = dof_pos[dof_start:dof_start + dof_size]
        
        if dof_size == 3:
            joint_pose_q = quat_from_euler_xyz(*joint_pose)

            # print(joint_pose_q)
        elif dof_size == 1:
            axis = torch.tensor([0.0, 1.0, 0.0], dtype=joint_pose.dtype, device=joint_pose.device)
            joint_pose_q = quat_from_angle_axis(joint_pose[..., 0], axis)
        else:
            assert False, "Unsupported joint type"

        non_root_joint_rot.append(joint_pose_q)

    
    # prepare data cat pos and rot
    # make non_root_joint_rot to be a numpy shape (13, 4)
    output = {
        'root_joint': root_pos_and_rot.cpu().numpy(),
        'non_root_joints_rot': np.array([non_root_joint_rot[i].cpu().numpy() for i in range(len(non_root_joint_rot))])
    }
    # print(output)
    # np.save('one_frame.npy', output)

    # 获取当前时间戳
    file_path = 'state_timestamp'+ '.csv'
    flat_data = output['root_joint'].tolist() + output['non_root_joints_rot'].flatten().tolist()

    # # if csv file not exist, create it and write header
    # # if not os.path.exists(file_path):
    # #     with open(file_path, 'a+') as csv_file:
    # #         writer = csv.writer(csv_file)
    # #         writer.writerow(header)
    
    # write data to csv file
    with open(file_path, 'a+') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(flat_data)

    return