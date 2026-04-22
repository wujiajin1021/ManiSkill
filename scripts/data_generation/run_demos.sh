export PYTHONPATH=/home/ps/Documents/ManiSkill/mani_skill:$PYTHONPATH
cd ../../

process_trajectory() {
  local traj_path="$1"
  local count="$2"
  local _data_dir="$3"
  local backend="$4"

  echo "Processing $traj_path"
  python mani_skill/trajectory/rbs_replay_trajectory.py --traj-path "$traj_path" -n 10 --count "$count" --use-env-states -b "$backend" --save_traj --output-dir "$_data_dir" -o 'rgb+depth+segmentation' --record-id-poses --record_id_mesh_info --postprocess-camera-data --postprocess-workers 1 --postprocess-delete-npy
}
# process_trajectory "/mnt/ManiSkill/demos/history_data/172.16.0.134/PickCubeSO100-v1/motionplanning/20260123_201416.h5" "1000" "/mnt/ManiSkill/demos/history_data/172.16.0.134/PickCubeSO100-v1/motionplanning" "auto"
# process_trajectory "/mnt/ManiSkill/demos/history_data/172.16.0.134/PickCube-v1_xarm6/motionplanning/20260123_202222.h5" "1000" "/mnt/ManiSkill/demos/history_data/172.16.0.134/PickCube-v1_xarm6/motionplanning" "auto"
# process_trajectory "/mnt/ManiSkill/demos/history_data/172.16.0.134/PlaceSphere-v1/motionplanning/20260123_194259.h5" "1000" "/mnt/ManiSkill/demos/history_data/172.16.0.134/PlaceSphere-v1/motionplanning" "auto"

# process_trajectory "/mnt/ManiSkill/demos/history_data/172.16.0.134/PickCube-v1_panda/motionplanning/20260123_175448.h5" "100" "/mnt/Object_World_Dataset/maniskill_data/PickCube-v1_panda/motionplanning" "auto"
# process_trajectory "/mnt/ManiSkill/demos/history_data/172.16.0.134/PushCube-v1_panda/motionplanning/20260123_180015.h5" "100" "/mnt/Object_World_Dataset/maniskill_data/PushCube-v1_panda/motionplanning" "auto"
process_trajectory "/mnt/ManiSkill/demos/history_data/172.16.0.134/StackCube-v1_panda/motionplanning/20260123_180412.h5" "100" "/mnt/Object_World_Dataset/maniskill_data/StackCube-v1_panda/motionplanning" "auto"


# process_trajectory "/mnt/ManiSkill/demos/PlugCharger-v1/motionplanning/trajectory.h5" "/mnt/ManiSkill/demos/PlugCharger-v1/motionplanning" "auto"
# process_trajectory "/mnt/ManiSkill/demos/PokeCube-v1/rl/trajectory.none.pd_ee_delta_pose.physx_cuda.h5" "/mnt/ManiSkill/demos/PokeCube-v1/rl" "auto"
# process_trajectory "/mnt/ManiSkill/demos/PullCubeTool-v1/motionplanning/trajectory.h5" "/mnt/ManiSkill/demos/PullCubeTool-v1/motionplanning" "auto"
# process_trajectory "/mnt/ManiSkill/demos/PushCube-v1/rl/trajectory.none.pd_ee_delta_pos.physx_cuda.h5" "/mnt/ManiSkill/demos/PushCube-v1/rl" "auto"
# process_trajectory "/mnt/ManiSkill/demos/PushT-v1/rl/trajectory.none.pd_ee_delta_pose.physx_cuda.h5" "/mnt/ManiSkill/demos/PushT-v1/rl" "auto"
# process_trajectory "/mnt/ManiSkill/demos/StackCube-v1/rl/trajectory.none.pd_ee_delta_pos.physx_cuda.h5" "/mnt/ManiSkill/demos/StackCube-v1/rl" "auto"
# process_trajectory "/mnt/ManiSkill/demos/StackPyramid-v1/motionplanning/trajectory.h5" "/mnt/ManiSkill/demos/StackPyramid-v1/motionplanning" "auto"
echo "All tasks finished."