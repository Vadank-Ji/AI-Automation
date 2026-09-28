import yaml
import time

while True:
    with open("../config/app_config.yml") as f:
        config = yaml.safe_load(f)
    print(f"Current Model: {config['model']}")
    time.sleep(5)