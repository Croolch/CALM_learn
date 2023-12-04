from poselib.visualization.common import plot_skeleton_motion_interactive, plot_skeleton_state
from poselib.skeleton.skeleton3d import SkeletonMotion, SkeletonState


def main():
    # pose = SkeletonState.from_file("data/cmu_tpose.npy")
    # motion = SkeletonMotion.from_file("data/RL_Avatar_WalkRight02_Motion.npy")
    motion = SkeletonMotion.from_fbx("mydata/D1_013_KAN01_001.fbx")
    # save motion
    motion.to_file("mydata/D1_013_KAN01_001.npy")
    plot_skeleton_motion_interactive(motion)
    

main()