import yaml
import os
from pathlib import Path

DEFAULT_CFG = os.path.join(str(Path.home()), 'configs', 'config.yml')


def get_config(cfg_path=None):
    cfg_path = cfg_path or DEFAULT_CFG
    with open(cfg_path) as f:
        cfg = yaml.safe_load(f)
    return cfg
