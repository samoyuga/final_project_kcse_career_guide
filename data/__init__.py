"""
KCSE Career Guidance Tool - Data Package

This package contains data files and configurations for the career guidance system:
- career_paths.json: Career database with requirements and information
"""

__version__ = "1.0.0"

# Import data loading functions
from .career_paths import load_career_data, get_career_clusters

__all__ = [
    'load_career_data',
    'get_career_clusters'
]

def initialize_data():
    """
    Initialize and validate data files.
    """
    try:
        from .career_paths import validate_career_data
        is_valid = validate_career_data()
        if is_valid:
            print("✅ Career data validated successfully")
            return True
        else:
            print("❌ Career data validation failed")
            return False
    except Exception as e:
        print(f"❌ Error initializing data: {e}")
        return False