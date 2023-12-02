# 把csv中的position与rotation转变为blender中的position与rotation，以csv表头的名字对应为blender中objects的名字
# import bpy
import csv
import os

# read csv file
csv_path = "/home/chen/Desktop/code/CALM/state_timestamp.csv"
csv_file = open(csv_path, "r")
reader = csv.reader(csv_file)
# get the header
header = next(reader)
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

# get body number
body_num = int(len(header) / 7)
# get body name
body_name = []
for i in range(body_num):
    # header取出字符串，按照_分割，删去最后两个元素，再按照_连接
    body_name.append("_".join(header[i * 7].split("_")[:-2]))


# get body statefrom data (frame, body_num, 7)
body_state = []
for i in range(len(data)):
    body_state.append([])
    for j in range(body_num):
        body_state[i].append(data[i][j * 7 : (j + 1) * 7])


# create objects based on body name
for i in range(body_num):
    bpy.ops.mesh.primitive_cube_add(size = 0.1, enter_editmode = False, location = (0, 0, 0))
    bpy.context.object.name = body_name[i]
    bpy.context.object.rotation_mode = 'QUATERNION'

# set keyframe
for i in range(len(body_state)):
    for j in range(body_num):
        bpy.data.objects[body_name[j]].location = (float(body_state[i][j][0]), float(body_state[i][j][1]), float(body_state[i][j][2]))
        bpy.data.objects[body_name[j]].rotation_quaternion = (float(body_state[i][j][3]), float(body_state[i][j][4]), float(body_state[i][j][5]), float(body_state[i][j][6]))
        bpy.data.objects[body_name[j]].keyframe_insert(data_path = "location", frame = i)
        bpy.data.objects[body_name[j]].keyframe_insert(data_path = "rotation_quaternion", frame = i)
