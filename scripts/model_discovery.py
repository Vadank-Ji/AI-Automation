import os
import requests
import sys
import json
from datetime import datetime, timezone
from dotenv import load_dotenv
import re

load_dotenv()

API_URL = "https://api.openai.com/v1/models"


# Models belonging to specialized capabilities
EXCLUDED_PATTERNS = [
    "image",
    "audio",
    "realtime",
    "transcribe",
    "tts",
    "embedding",
    "moderation",
    "search",
    "codex",
    "deep-research",
    "computer-use",
    "live"
]


def is_eligible_model(model):

    model_id = model["id"].lower()

    # Only consider GPT models
    if not model_id.startswith("gpt-"):
        return False

    # Exclude specialized models
    for pattern in EXCLUDED_PATTERNS:
        if pattern in model_id:
            return False

    # Exclude preview models
    if "preview" in model_id:
        return False

    # Exclude models that have a shutdown date
    if model.get("shutdown_date"):
        return False
    if re.search(r"-\d{4}-\d{2}-\d{2}$", model_id):
        return False

    return True


def get_available_models():

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.get(
        API_URL,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    return response.json()["data"]


try:

    models = get_available_models()

    eligible_models = [
        model
        for model in models
        if is_eligible_model(model)
    ]

    # Newer models are assumed to have a later creation timestamp
    eligible_models.sort(
        key=lambda model: model["created"],
        reverse=True
    )

    result = {
        "eligible_models": [
            model["id"]
            for model in eligible_models
        ],
        "latest_model": (
            eligible_models[0]["id"]
            if eligible_models
            else None
        )
    }

    print(json.dumps(result))


except Exception as e:

    print(json.dumps({
        "error": str(e)
    }))

    sys.exit(1)