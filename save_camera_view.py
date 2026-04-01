"""
Interactive Camera Configuration Tool for ManiSkill

This script allows you to:
1. Create an environment with gym.make()
2. Open the SAPIEN Viewer and freely adjust the camera view with your mouse
3. Press 'P' to save the current viewer camera's eye position and target
4. Press 'R' to reset the camera to default position
5. Press 'ESC' to exit and save all configurations

Usage:
    python scripts/save_camera_view.py -e PickCube-v1
    
    # Then in the viewer window:
    # - Use mouse to adjust camera view
    # - Press 'P' to save current camera configuration
    # - Press 'R' to reset camera
    # - Press 'ESC' to exit
"""

import argparse
import json
import os
from datetime import datetime

import gymnasium as gym
import numpy as np
import sapien

from mani_skill.envs.sapien_env import BaseEnv


def parse_args():
    parser = argparse.ArgumentParser(
        description="Interactive camera configuration tool for ManiSkill"
    )
    parser.add_argument(
        "-e", "--env-id", type=str, default="PushCube-v1", help="Environment ID"
    )
    parser.add_argument(
        "-o", "--obs-mode", type=str, default="state", help="Observation mode"
    )
    parser.add_argument(
        "--control-mode", type=str, default="pd_ee_delta_pose", help="Control mode"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="camera_configs",
        help="Directory to save camera configs",
    )
    args = parser.parse_args()
    return args


class CameraConfigRecorder:
    def __init__(self, env: BaseEnv, env_id: str, output_dir: str = "camera_configs"):
        self.env = env
        self.env_id = env_id
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # Get the unwrapped environment to access internal attributes
        self.unwrapped_env = env.unwrapped if hasattr(env, 'unwrapped') else env

        # Get viewer
        viewer = getattr(self.unwrapped_env, 'viewer', None) or getattr(self.unwrapped_env, '_viewer', None)
        if viewer is None:
            raise ValueError(
                "Environment does not have a viewer. Make sure render_mode='human'"
            )

        self.viewer = viewer
        self.saved_configs = []

        # Get base_camera if it exists for reference
        self.base_camera = None
        if hasattr(self.unwrapped_env, '_sensors') and "base_camera" in self.unwrapped_env._sensors:
            self.base_camera = self.unwrapped_env._sensors["base_camera"]

        print("=" * 70)
        print("Interactive Camera Configuration Tool")
        print("=" * 70)
        print("\nControls:")
        print("  Mouse:        Rotate and move camera view")
        print("  Mouse Wheel:  Zoom in/out")
        print("  P:            Save current camera configuration")
        print("  R:            Reset camera to default position")
        print("  I:            Print current camera info")
        print("  ESC:          Exit and save all configurations")
        print("=" * 70)
        print()

    def get_camera_pose(self):
        """Get current viewer camera pose"""
        # Get camera pose from the viewer window (this is the interactive camera)
        camera_pose = self.viewer.window.get_camera_pose()
        
        # Extract position (eye) from the pose
        eye = np.array(camera_pose.p)
        
        # Get camera forward direction and calculate target
        # SAPIEN camera forward direction is x-axis
        forward = camera_pose.to_transformation_matrix()[:3, 0]
        
        # Target is some distance in front of the camera
        # We use a default distance of 1.0 meter
        distance = 1.0
        target = eye + forward * distance
        
        return eye, target

    def print_camera_config(self):
        """Print current camera configuration"""
        eye, target = self.get_camera_pose()
        print("\n" + "=" * 70)
        print("Current Camera Configuration:")
        print("-" * 70)
        print(f"Eye (Camera Position):")
        print(f"  [{eye[0]:.4f}, {eye[1]:.4f}, {eye[2]:.4f}]")
        print(f"\nTarget (Looking At):")
        print(f"  [{target[0]:.4f}, {target[1]:.4f}, {target[2]:.4f}]")
        distance = np.linalg.norm(target - eye)
        print(f"\nDistance to Target: {distance:.4f}")
        print(f"Saved Configurations: {len(self.saved_configs)}")
        print("=" * 70)

    def save_config(self):
        """Record current camera configuration (not saved to file yet)"""
        eye, target = self.get_camera_pose()

        # Simply store [eye, target] pair
        config = [eye.tolist(), target.tolist()]
        self.saved_configs.append(config)

        print(f"\n✓ Camera configuration #{len(self.saved_configs)} recorded")
        self.print_camera_config()

    def save_all_configs(self):
        """Save all recorded configurations to a single file"""
        if not self.saved_configs:
            print("\nNo configurations were saved during this session.")
            return

        filename = os.path.join(self.output_dir, f"camera_{self.env_id}.json")
        with open(filename, "w") as f:
            json.dump(self.saved_configs, f, indent=2)

        print(f"\n✓ All {len(self.saved_configs)} configurations saved to: {filename}")


def main():
    args = parse_args()

    print(f"\nCreating environment: {args.env_id}")
    print("Render mode: human (with viewer)")
    
    env: BaseEnv = gym.make(
        args.env_id,
        obs_mode=args.obs_mode,
        control_mode=args.control_mode,
        render_mode="human",  # Must be human to have viewer
    )

    # Reset environment
    obs, info = env.reset()

    # Render once to create the viewer
    env.render()

    # Create recorder
    try:
        recorder = CameraConfigRecorder(env, env_id=args.env_id, output_dir=args.output_dir)
    except ValueError as e:
        print(f"Error: {e}")
        env.close()
        return

    # Print initial camera info
    recorder.print_camera_config()

    # Main loop
    print("\nViewer window is now open. Adjust the camera and press 'P' to save.")
    print("Press 'I' to print current camera info.")
    print("Press 'ESC' to exit.\n")

    try:
        while True:
            # Render environment
            env.render()

            # Check for key presses
            if recorder.viewer.window.key_down("p"):
                recorder.save_config()
                # Small delay to avoid multiple saves
                import time
                time.sleep(0.3)

            elif recorder.viewer.window.key_down("i"):
                recorder.print_camera_config()
                import time
                time.sleep(0.3)

            elif recorder.viewer.window.key_down("escape"):
                print("\nExiting...")
                break

            # Small sleep to prevent busy loop
            import time
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\n\nInterrupted by user (Ctrl+C)")

    finally:
        # Save all configurations
        recorder.save_all_configs()
        env.close()
        print("\nEnvironment closed. Goodbye!")


if __name__ == "__main__":
    main()
