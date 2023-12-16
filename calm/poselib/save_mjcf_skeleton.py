from poselib.skeleton.skeleton3d import SkeletonTree
import numpy as np

sk = SkeletonTree.from_mjcf("../data/assets/mjcf/amp_humanoid_sword_shield.xml")

sk_dict = {"node_names": sk.node_names, "parent_indices": sk.parent_indices.numpy(), "local_translation": sk.local_translation.numpy()}
np.save("armature.npy", sk_dict)
