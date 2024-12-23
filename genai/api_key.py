"""Provides access to the Gemini API key via environment variables."""

from os import environ

API_KEY_NAME = "GEMINI_API_KEY"

api_key = environ.get(API_KEY_NAME)
