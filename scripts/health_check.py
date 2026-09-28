import yaml
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "../config/app_config.yml")

try:
    with open(CONFIG_PATH) as f:
        config = yaml.safe_load(f)

    if not config:
        raise ValueError("Configuration is empty")

    elif "model" not in config:
        raise ValueError("Model configuration is missing")

    elif not config["model"]:
        raise ValueError("Model is missing from configuration")

    print(f"Current Model: {config['model']}")

    # TEMPORARY FAILURE TEST
    if config["model"] == "gpt-5.6":
        raise ValueError("Simulated failure for upgraded model")

    print("AI Service: Healthy")

    sys.exit(0)

except Exception as e:
    print(f"AI Service: UNHEALTHY - {e}")
    sys.exit(1)