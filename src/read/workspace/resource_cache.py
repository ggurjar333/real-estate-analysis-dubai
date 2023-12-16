import read.logging_helpers
from typing import NamedTuple, Any
logging = read.logging_helpers.get_logger(__name__)


class ReadResourceKey(NamedTuple):
    """Uniquely identifies a specific resource. """
    dataset: str
    doi: str
    name: str

    def __repr__(self) -> str:
        """Returns string representation of ReadResourceKey."""
        return f"Resource({self.dataset}/{self.doi}/{self.name})"

