"""Datastore manages data retrieval for READ datasets."""
import read

logger = read.logging_helpers.get_logger(__name__)


class HuspyFetcher:
    """API for fetching contents from Huspy."""

    def __init__(self):
