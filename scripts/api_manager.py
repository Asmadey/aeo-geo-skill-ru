#!/usr/bin/env python3
"""
api_manager.py — API Manager for AEO Skill.

Manages external service integrations (OpenAI, Anthropic, Gemini, Perplexity,
Ahrefs, SEMrush) with graceful fallback to offline heuristic analysis when
API keys are not provided.
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("aeo.api_manager")


class RateLimiter:
    """Simple in-memory sliding window rate limiter."""

    def __init__(self, max_requests: int, time_window_seconds: int):
        self.max_requests = max_requests
        self.time_window = time_window_seconds
        self.requests: List[datetime] = []

    def can_request(self) -> bool:
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(seconds=self.time_window)
        self.requests = [t for t in self.requests if t > cutoff]
        return len(self.requests) < self.max_requests

    def wait_if_needed(self):
        while not self.can_request():
            time.sleep(0.1)
        self.requests.append(datetime.now(timezone.utc))


class APIManager:
    """
    Manages external API integrations with graceful degradation.
    Works 100% offline without external keys, enabling local heuristic analysis.
    """

    SUPPORTED_KEYS = [
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "GEMINI_API_KEY",
        "PERPLEXITY_API_KEY",
        "AHREFS_API_KEY",
        "SEMRUSH_API_KEY",
    ]

    def __init__(self, config_file: Optional[Path] = None):
        self.config: Dict[str, str] = {}
        self.config_file = config_file or Path.home() / ".aeo-data" / "api_config.json"
        self._load_keys()

        self.rate_limiters = {
            "openai": RateLimiter(max_requests=60, time_window_seconds=60),
            "anthropic": RateLimiter(max_requests=50, time_window_seconds=60),
            "perplexity": RateLimiter(max_requests=30, time_window_seconds=60),
            "gemini": RateLimiter(max_requests=60, time_window_seconds=60),
            "ahrefs": RateLimiter(max_requests=1, time_window_seconds=1),
            "semrush": RateLimiter(max_requests=10, time_window_seconds=60),
        }

    def _load_keys(self):
        # 1. From local config file if exists
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    file_conf = json.load(f)
                    if isinstance(file_conf, dict):
                        self.config.update(file_conf)
            except Exception as e:
                logger.warning(f"Could not load {self.config_file}: {e}")

        # 2. From environment variables (override config file)
        for key in self.SUPPORTED_KEYS:
            env_val = os.getenv(key)
            if env_val:
                self.config[key] = env_val.strip()

    def has_key(self, key_name: str) -> bool:
        return bool(self.config.get(key_name, "").strip())

    def get_key(self, key_name: str) -> Optional[str]:
        return self.config.get(key_name)

    def set_key(self, key_name: str, key_value: str) -> bool:
        if key_name not in self.SUPPORTED_KEYS:
            logger.error(f"Unsupported key name: {key_name}")
            return False
        self.config[key_name] = key_value.strip()
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to persist key: {e}")
            return False

    def status(self) -> Dict[str, Any]:
        return {
            "mode": "hybrid" if any(self.has_key(k) for k in self.SUPPORTED_KEYS) else "offline-heuristic",
            "available_apis": {
                key: ("configured" if self.has_key(key) else "missing (using local heuristic)")
                for key in self.SUPPORTED_KEYS
            },
        }

    def with_fallback(self, primary_func: Callable, fallback_func: Callable, api_name: str) -> Any:
        key_name = f"{api_name.upper()}_API_KEY"
        if self.has_key(key_name):
            try:
                if api_name in self.rate_limiters:
                    self.rate_limiters[api_name].wait_if_needed()
                return primary_func()
            except Exception as e:
                logger.warning(f"{api_name} API failed ({e}), falling back to local heuristic.")
                return fallback_func()
        return fallback_func()


def main():
    parser = argparse.ArgumentParser(description="AEO API Configuration & Status Manager")
    parser.add_argument("--status", action="store_true", help="Show API configuration status")
    parser.add_argument("--set", nargs=2, metavar=("KEY_NAME", "VALUE"), help="Store an API key locally")
    args = parser.parse_args()

    manager = APIManager()

    if args.set:
        key_name, val = args.set
        if manager.set_key(key_name, val):
            print(f"✅ Stored {key_name} successfully.")
        else:
            sys.exit(1)
        return

    # Default action: status
    status = manager.status()
    print("=== AEO API Integration Status ===")
    print(f"Operational Mode: {status['mode']}")
    print("\nAPI Keys:")
    for k, v in status["available_apis"].items():
        icon = "🟢" if "configured" in v else "⚪"
        print(f"  {icon} {k:<20} {v}")


if __name__ == "__main__":
    main()
