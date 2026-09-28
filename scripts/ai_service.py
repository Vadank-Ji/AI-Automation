#!/usr/bin/env python3
"""Interactive Groq service and deployment health check."""

import argparse
import os
import sys
import time
from pathlib import Path

import yaml
from dotenv import load_dotenv
from groq import Groq


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_PATH = PROJECT_DIR / "config" / "app_config.yml"
ENV_PATH = SCRIPT_DIR / ".env"

load_dotenv(ENV_PATH)


def load_config():
    """Load and validate the service configuration."""
    with CONFIG_PATH.open(encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file) or {}

    model = config.get("model")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Model configuration is missing")

    temperature = config.get("temperature", 0.7)
    if not isinstance(temperature, (int, float)) or not 0 <= temperature <= 2:
        raise ValueError("Temperature must be a number between 0 and 2")

    return config


def create_client():
    """Create the API client from the local environment."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing")
    return Groq(api_key=api_key)


def health_check():
    """Make a small real request and return a shell-compatible exit code."""
    try:
        config = load_config()
        client = create_client()
        client.chat.completions.create(
            model=config["model"],
            messages=[{"role": "user", "content": "Reply with OK."}],
            temperature=0,
            max_tokens=2,
        )
    except Exception as error:
        print(f"Health check failed: {error}", file=sys.stderr)
        return 1

    print(f"Health check passed for model {config['model']}")
    return 0


def run_interactive():
    """Run the interactive chat loop."""
    config = load_config()
    client = create_client()
    model = config["model"]
    temperature = config.get("temperature", 0.7)

    print("AIIAU AI SERVICE")
    print(f"Provider: Groq\nModel: {model}\n")
    print("Type 'exit' to stop.")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nShutting down AI service...")
            return

        if user_input.lower() == "exit":
            print("Shutting down AI service...")
            return
        if not user_input:
            continue

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": user_input}],
                temperature=temperature,
            )
            answer = response.choices[0].message.content or ""
            print(f"AI: {answer}")
        except Exception as error:
            print(f"AI service error: {error}", file=sys.stderr)


def run_daemon():
    """Keep a lightweight health-monitor process running for Ansible."""
    interval = 60
    print(f"AIIAU health monitor started; checking every {interval} seconds.")
    while True:
        health_check()
        time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--health",
        action="store_true",
        help="make a real API request and return its status",
    )
    mode.add_argument(
        "--daemon",
        action="store_true",
        help="run a periodic health-monitor process",
    )
    args = parser.parse_args()

    if args.health:
        return health_check()
    if args.daemon:
        run_daemon()
        return 0

    run_interactive()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())