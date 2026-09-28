import os
import requests
from dotenv import load_dotenv

# --------------------------------------------------
# Paths
# --------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, ".env")

load_dotenv(ENV_PATH)


# --------------------------------------------------
# Groq API configuration
# --------------------------------------------------

API_URL = "https://api.groq.com/openai/v1/models"

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found. "
        "Make sure it is inside scripts/.env"
    )

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}


# --------------------------------------------------
# Get models from Groq
# --------------------------------------------------

def get_models():

    response = requests.get(
        API_URL,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return data.get("data", [])


# --------------------------------------------------
# Filter models
# --------------------------------------------------

def is_text_model(model):

    model_id = model.get("id", "").lower()

    if not model_id:
        return False

    # Ignore audio / speech models
    excluded_patterns = [
        "whisper",
        "audio",
        "tts",
        "transcribe",
        "speech"
    ]

    for pattern in excluded_patterns:

        if pattern in model_id:
            return False

    return True


# --------------------------------------------------
# Display models
# --------------------------------------------------

def display_models(models):

    print()
    print("=" * 65)
    print("              GROQ MODEL DISCOVERY")
    print("=" * 65)
    print()

    for index, model in enumerate(models, start=1):

        model_id = model.get("id")
        owner = model.get("owned_by", "Unknown")
        context = model.get("context_window", "Unknown")

        print(
            f"{index}. {model_id}"
        )

        print(
            f"   Owner: {owner}"
        )

        print(
            f"   Context Window: {context}"
        )

        print()


# --------------------------------------------------
# Select model
# --------------------------------------------------

def select_model(models):

    while True:

        choice = input(
            "Enter the number of the model you want to use: "
        ).strip()

        try:

            index = int(choice)

            if 1 <= index <= len(models):

                selected = models[index - 1]

                return selected["id"]

            print(
                f"Please enter a number between 1 and {len(models)}."
            )

        except ValueError:

            print("Please enter a valid number.")


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    try:

        models = get_models()

        text_models = [
            model
            for model in models
            if is_text_model(model)
        ]

        if not text_models:

            print("No suitable text models were found.")
            return

        display_models(text_models)

        selected_model = select_model(text_models)

        print()
        print("=" * 65)
        print("MODEL SELECTED")
        print("=" * 65)
        print()
        print(f"Model: {selected_model}")
        print()

        print(
            "Put this model into config/app_config.yml:"
        )

        print()
        print(f"model: {selected_model}")
        print("temperature: 0.7")
        print("gpu: false")
        print("port: 8000")
        print()

    except requests.exceptions.HTTPError as e:

        print()
        print("Groq API Error:")
        print(e)

    except requests.exceptions.RequestException as e:

        print()
        print("Network Error:")
        print(e)

    except Exception as e:

        print()
        print("Error:")
        print(e)


if __name__ == "__main__":
    main()