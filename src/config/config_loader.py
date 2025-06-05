import yaml
import os
def load_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))  # => src/config
    config_path = os.path.join(current_dir, "config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)