import json
import yaml
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "../config/app_config.yml")

LATEST_APPROVED_MODEL="gpt-5.6"

with open(CONFIG_PATH) as file:
    config = yaml.safe_load(file)

current_model = config["model"]

result={
    "current_model":current_model,
    "latest_model": LATEST_APPROVED_MODEL,
    "update_available": (
        current_model != LATEST_APPROVED_MODEL
    )
}

print(json.dumps(result))