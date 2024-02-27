import mujoco

mjcf_filepath = "../calm/data/assets/mjcf/amp_humanoid_sword_shield.xml"
m = mujoco.MjModel.from_xml_path(mjcf_filepath)
d = mujoco.MjData(m)

mesh_face = m.mesh_face.tolist()
print(mesh_face)