import json
import random
import re
from pathlib import Path
from typing import List

import torch

from mani_skill.utils import sapien_utils
from mani_skill.utils.structs import Pose


def _extract_registered_env_ids(task_file: Path) -> List[str]:
    try:
        src = task_file.read_text()
    except Exception:
        return []
    matches = re.findall(r"@register_env\(\s*[\"']([^\"']+)[\"']", src)
    seen = set()
    env_ids = []
    for m in matches:
        if m in seen:
            continue
        seen.add(m)
        env_ids.append(m)
    return env_ids


def _load_camera_pairs(task_file: str) -> List[list]:
    file_path = Path(task_file).resolve()
    task_name = file_path.stem
    root = file_path.parents[4]
    env_ids = _extract_registered_env_ids(file_path)

    candidates = []
    for env_id in env_ids:
        candidates.append(root / "camera_configs" / f"camera_{env_id}.json")
        candidates.append(root / f"camera_{env_id}.json")

    candidates += [
        root / "camera_configs" / f"camera_{task_name}.json",
        root / f"camera_{task_name}.json",
        root / "camera_configs" / "camera_config.json",
        root / "camera_config.json",
    ]

    for cfg in candidates:
        if cfg.exists():
            pairs = json.loads(cfg.read_text())
            if isinstance(pairs, list) and len(pairs) > 0:
                return pairs

    searched = "\n  - ".join(str(p) for p in candidates)
    raise FileNotFoundError(
        "No valid camera config found. Searched:\n  - " + searched
    )


def build_tabletop_base_camera_pose(task_file: str, num_envs: int) -> Pose:
    pairs = _load_camera_pairs(task_file)

    if int(num_envs) == 1:
        eye, target = random.choice(pairs)
        return sapien_utils.look_at(eye=eye, target=target)

    n = int(num_envs)
    picks = [random.choice(pairs) for _ in range(n)]
    poses = [sapien_utils.look_at(eye=p[0], target=p[1]) for p in picks]
    raws = [p.raw_pose.view(-1) for p in poses]
    return Pose.create(torch.stack(raws, dim=0))
