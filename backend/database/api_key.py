"""Provides access to the Pinecone API key via environment variables."""

from os import environ

API_KEY_NAME = "PINECONE_API_KEY"

api_key = environ.get(API_KEY_NAME)
