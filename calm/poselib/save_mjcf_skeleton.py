import xml.etree.ElementTree as ET
import numpy as np

def generate_joints_from_mjcf(path: str):
    """
    Parses a mujoco xml scene description file and returns a Skeleton Tree.
    We use the model attribute at the root as the name of the tree.
    
    :param path:
    :type path: string
    :return: The skeleton tree constructed from the mjcf file
    :rtype: SkeletonTree
    """
    tree = ET.parse(path)
    xml_doc_root = tree.getroot()
    xml_world_body = xml_doc_root.find("worldbody")
    if xml_world_body is None:
        raise ValueError("MJCF parsed incorrectly please verify it.")
    # assume this is the root
    xml_body_root = xml_world_body.find("body")
    if xml_body_root is None:
        raise ValueError("MJCF parsed incorrectly please verify it.")

    node_names = []
    parent_indices = []
    local_translation = []
    joint_names = []
    joint_parent_indices = []
    joint_local_translation = []

    # adding joint nodes
    def _add_xml_joint_node(xml_node, parent_index):
        # find joint from subnode
        joint_node = xml_node.find("joint")
        if joint_node is None:
            joint_node = xml_node.find("freejoint")

        if joint_node is None:
            joint_names.append("none")
            joint_parent_indices.append(parent_index)
            joint_local_translation.append(np.zeros(3))
            return
        
        # assert joint_node is not None, "No joint found in the body node."

        joint_parent_indices.append(parent_index)
        joint_name = joint_node.attrib.get("name")
        if joint_name[-2:] in ["_x", "_y", "_z"]:
            joint_name = joint_name[:-2]
        print("adding joint name: ", joint_name)
        joint_names.append(joint_name)
        joint_pos_str = joint_node.attrib.get("pos")
        if joint_pos_str is not None:
            joint_pos = np.fromstring(joint_pos_str, dtype=float, sep=" ")
            joint_local_translation.append(joint_pos)
        else:
            joint_local_translation.append(np.zeros(3))
    
    # post process the joint nodes
    def _joint_postprocess():
        # compress the joint nodes indices
        # add body translation to the joint local translation
        for i in range(len(joint_parent_indices)):
            joint_local_translation[i] += local_translation[i]

    # recursively adding all nodes into the skel_tree
    def _add_xml_node(xml_node, parent_index, node_index):
        node_name = xml_node.attrib.get("name")
        # parse the local translation into float list
        pos = np.fromstring(xml_node.attrib.get("pos"), dtype=float, sep=" ")
        node_names.append(node_name)
        parent_indices.append(parent_index)
        local_translation.append(pos)

        _add_xml_joint_node(xml_node, parent_index)

        curr_index = node_index
        node_index += 1
        for next_node in xml_node.findall("body"):
            node_index = _add_xml_node(next_node, curr_index, node_index)
        return node_index

    _add_xml_node(xml_body_root, -1, 0)

    _joint_postprocess()

    return {
        "node_names": node_names,
        "parent_indices": parent_indices,
        "local_translation": local_translation,
        "joint_names": joint_names,
        "joint_parent_indices": joint_parent_indices,
        "joint_local_translation": joint_local_translation,
    }

sk_dict = generate_joints_from_mjcf("../data/assets/mjcf/amp_humanoid_sword_shield.xml")

print(sk_dict["joint_parent_indices"])
np.save("armature.npy", sk_dict)
