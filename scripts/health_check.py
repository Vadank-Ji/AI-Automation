#!/usr/bin/env python3
"""Compatibility entry point for the AIIAU real AI health check."""

from ai_service import health_check


if __name__ == "__main__":
    raise SystemExit(health_check())
