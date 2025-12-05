
"""
Utility dictionary helpers.
This module is optional and does not affect any existing functionality.
"""

def safe_get(dictionary, key, default=None):
    """
    Safely get a key from a dictionary.
    If the key does not exist, returns the default value.
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key, default)
    return default

def merge_dicts(*dicts):
    """
    Safely merges multiple dictionaries into a new one.
    Later dictionaries override earlier ones.
    """
    result = {}
    for d in dicts:
        if isinstance(d, dict):
            result.update(d)
    return result

# A simple placeholder dictionary (harmless)
DEFAULT_INFO = {
    "version": "1.0",
    "description": "Dictionary utilities for optional use.",
}
