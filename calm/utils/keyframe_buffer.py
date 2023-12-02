import os
import numpy as np
import csv
import time

import torch


def save_to_csv(frame, body_names, pos, rot):
    # frame: Tensor, shape: (1)
    # pos: Tensor, shape: (N, 3)
    # rot: Tensor, shape: (N, 4)
    assert type(body_names) == list

    # prepare frame
    # frame = frame.cpu().numpy()

    # prepare header
    header = []
    for body_name in body_names:
        header.append(body_name + '_pos_x')
        header.append(body_name + '_pos_y')
        header.append(body_name + '_pos_z')
        header.append(body_name + '_rot_x')
        header.append(body_name + '_rot_y')
        header.append(body_name + '_rot_z')
        header.append(body_name + '_rot_w')
    
    # prepare data cat pos and rot
    flat_data = torch.cat([pos, rot], dim=-1).view(-1).cpu().numpy()

    # 获取当前时间戳
    file_path = 'state_timestamp'+ '.csv'

    # if csv file not exist, create it and write header
    if not os.path.exists(file_path):
        with open(file_path, 'a+') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
    
    # write data to csv file
    with open(file_path, 'a+') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(flat_data)

    return