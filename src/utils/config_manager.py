import yaml
import os

DEFAULT_CFG = os.path.join('/', 'config.yml')


def get_config(cfg_path=None):
    cfg_path = cfg_path or DEFAULT_CFG
    with open(cfg_path) as f:
        cfg = yaml.safe_load(f)
    return cfg


config = get_config()
