export PYTHONPATH=/home/ps/Documents/ManiSkill/mani_skill:$PYTHONPATH
cd ../../

process_trajectory() {
  local traj_path="$1"
  local _data_dir="$2"
  local backend="$3"

  echo "Processing $traj_path"
  python mani_skill/trajectory/rbs_replay_trajectory.py --traj-path "$traj_path" -n 10 --use-env-states -b "$backend" --save_traj -o 'rgb+depth+segmentation' --record-id-poses --record_id_mesh_info --postprocess-camera-data --postprocess-workers 1 --postprocess-delete-npy
}

# process_trajectory "/home/ps/.maniskill/demos/PegInsertionSide-v1/motionplanning/trajectory.h5" "/home/ps/.maniskill/demos/PegInsertionSide-v1/motionplanning" "auto"
process_trajectory "/home/ps/.maniskill/demos/PickCube-v1/motionplanning/trajectory.h5" "/home/ps/.maniskill/demos/PickCube-v1/motionplanning" "auto"
# process_trajectory "/home/ps/.maniskill/demos/PlugCharger-v1/motionplanning/trajectory.h5" "/home/ps/.maniskill/demos/PlugCharger-v1/motionplanning" "auto"
# process_trajectory "/home/ps/.maniskill/demos/PokeCube-v1/rl/trajectory.none.pd_ee_delta_pose.physx_cuda.h5" "/home/ps/.maniskill/demos/PokeCube-v1/rl" "auto"
# process_trajectory "/home/ps/.maniskill/demos/PullCubeTool-v1/motionplanning/trajectory.h5" "/home/ps/.maniskill/demos/PullCubeTool-v1/motionplanning" "auto"
# process_trajectory "/home/ps/.maniskill/demos/PullCube-v1/rl/trajectory.none.pd_ee_delta_pose.physx_cuda.h5" "/home/ps/.maniskill/demos/PullCube-v1/rl" "auto"
# process_trajectory "/home/ps/.maniskill/demos/PushCube-v1/motionplanning/trajectory.h5" "/home/ps/.maniskill/demos/PushCube-v1/motionplanning" "auto"
# process_trajectory "/home/ps/.maniskill/demos/PushT-v1/rl/trajectory.none.pd_ee_delta_pose.physx_cuda.h5" "/home/ps/.maniskill/demos/PushT-v1/rl" "auto"
# process_trajectory "/home/ps/.maniskill/demos/RollBall-v1/rl/trajectory.none.pd_ee_delta_pos.physx_cuda.h5" "/home/ps/.maniskill/demos/RollBall-v1/rl" "auto"
# process_trajectory "/home/ps/.maniskill/demos/StackCube-v1/motionplanning/trajectory.h5" "/home/ps/.maniskill/demos/StackCube-v1/motionplanning" "auto"
# process_trajectory "/home/ps/.maniskill/demos/StackPyramid-v1/motionplanning/trajectory.h5" "/home/ps/.maniskill/demos/StackPyramid-v1/motionplanning" "auto"
# process_trajectory "/home/ps/.maniskill/demos/TwoRobotPickCube-v1/rl/trajectory.none.pd_joint_delta_pos.physx_cuda.h5" "/home/ps/.maniskill/demos/TwoRobotPickCube-v1/rl" "auto"
# process_trajectory "/home/ps/.maniskill/demos/TwoRobotStackCube-v1/rl/trajectory.none.pd_joint_delta_pos.physx_cuda.h5" "/home/ps/.maniskill/demos/TwoRobotStackCube-v1/rl" "auto"
# process_trajectory "/home/ps/.maniskill/demos/LiftPegUpright-v1/rl/trajectory.none.pd_joint_delta_pos.physx_cuda.h5" "/home/ps/.maniskill/demos/LiftPegUpright-v1/rl" "auto"

echo "All tasks finished."