"""
KCSE Career Guidance Tool - Pages Package

This package contains all Streamlit pages for the application:
- Home.py: Landing page and introduction
- Career_Analysis.py: Subject and skills input form
- Payment.py: M-Pesa payment processing
- Results.py: Career recommendations and report
"""

__version__ = "1.0.0"

# List available pages for navigation
PAGES = {
    "Home": "1_🏠_Home.py",
    "Career Analysis": "2_📊_Career_Analysis.py", 
    "Payment": "3_💳_Payment.py",
    "Results": "4_📈_Results.py"
}

def get_page_path(page_name):
    """
    Get the file path for a page by its name.
    
    Args:
        page_name (str): Name of the page (e.g., "Home", "Career Analysis")
    
    Returns:
        str: File path for the page
    """
    return PAGES.get(page_name)

def get_all_pages():
    """
    Get all available pages.
    
    Returns:
        dict: Dictionary of page names and their file paths
    """
    return PAGES.copy()

__all__ = ['get_page_path', 'get_all_pages', 'PAGES']