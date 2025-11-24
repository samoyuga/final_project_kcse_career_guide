"""
KCSE Career Guidance Tool - Assets Package

This package contains static assets for the application:
- CSS stylesheets
- Images (future use)
- Icons (future use)
"""

__version__ = "1.0.0"

import os

def get_asset_path(filename):
    """
    Get the full path for an asset file.
    
    Args:
        filename (str): Name of the asset file
    
    Returns:
        str: Full path to the asset file
    """
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, filename)

def load_css(filename="style.css"):
    """
    Load and return CSS content as a string.
    
    Args:
        filename (str): CSS filename
    
    Returns:
        str: CSS content
    """
    try:
        css_path = get_asset_path(filename)
        with open(css_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"❌ Error loading CSS: {e}")
        return ""

__all__ = ['get_asset_path', 'load_css']