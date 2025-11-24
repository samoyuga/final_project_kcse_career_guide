"""
KCSE Career Guidance Tool - Utilities Package

This package contains all the utility modules for the career guidance system:
- database: Database operations and management
- career_engine: AI-powered career recommendation engine
- mpesa_integration: M-Pesa Daraja API integration
"""

__version__ = "1.0.0"
__author__ = "KCSE Career Guide Team"
__email__ = "support@kcsecareerguide.com"

# Import key functions for easier access
from .database import (
    init_db,
    save_user_data,
    save_payment,
    save_career_results,
    check_payment_status,
    get_user_data,
    get_payment_history,
    get_career_results,
    cleanup_old_data
)

from .career_engine import CareerEngine
from .mpesa_integration import process_mpesa_payment, MpesaDarajaAPI

# Define what gets imported with "from utils import *"
__all__ = [
    # Database functions
    'init_db',
    'save_user_data', 
    'save_payment',
    'save_career_results',
    'check_payment_status',
    'get_user_data',
    'get_payment_history',
    'get_career_results',
    'cleanup_old_data',
    
    # Career engine
    'CareerEngine',
    
    # M-Pesa integration
    'process_mpesa_payment',
    'MpesaDarajaAPI'
]

# Package initialization
print(f"Initializing KCSE Career Guide Utilities v{__version__}")

# You can add any package-level initialization code here
def initialize_utilities():
    """
    Initialize all utility modules.
    Call this at the start of your application.
    """
    try:
        # Initialize database
        from .database import init_db
        init_db()
        print("✅ Database initialized successfully")
        
        # You can add other initialization code here
        print("✅ All utilities initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing utilities: {e}")
        return False