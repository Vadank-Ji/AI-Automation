import os
import json

import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "../config/app_config.yml")

# Discovery and approval policy deliberately remain out of scope.  Change this
# only after approving a valid Groq chatbot model.
LATEST_APPROVED_MODEL = "openai/gpt-oss-20b"

with open(CONFIG_PATH, encoding="utf-8") as file:
    config = yaml.safe_load(file) or {}

current_model = config.get("model")
if not current_model:
    raise ValueError("Model configuration is missing")

result = {
    "current_model": current_model,
    "latest_model": LATEST_APPROVED_MODEL,
    "update_available": current_model != LATEST_APPROVED_MODEL,
}

print(json.dumps(result))
