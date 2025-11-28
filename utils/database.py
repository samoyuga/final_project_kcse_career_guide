import streamlit as st
import json
from datetime import datetime

def init_db():
    """Initialize session state for data storage"""
    if 'users' not in st.session_state:
        st.session_state.users = {}
    if 'user_subjects' not in st.session_state:
        st.session_state.user_subjects = {}
    if 'user_skills' not in st.session_state:
        st.session_state.user_skills = {}
    if 'user_interests' not in st.session_state:
        st.session_state.user_interests = {}
    if 'payments' not in st.session_state:
        st.session_state.payments = {}
    if 'career_results' not in st.session_state:
        st.session_state.career_results = {}
    if 'user_counter' not in st.session_state:
        st.session_state.user_counter = 0

def save_user_data(student_info, subjects_grades, skills_interests):
    """Save user data to session state and return user ID"""
    # Generate user ID
    st.session_state.user_counter += 1
    user_id = st.session_state.user_counter
    
    # Save user info
    st.session_state.users[user_id] = {
        'name': student_info['name'],
        'phone': student_info['phone'],
        'email': student_info.get('email', ''),
        'created_at': datetime.now().isoformat()
    }
    
    # Save subjects
    st.session_state.user_subjects[user_id] = {}
    for subject, grade in subjects_grades.items():
        if grade != "Not Taken" and grade != "Select Grade":
            st.session_state.user_subjects[user_id][subject] = grade
    
    # Save skills
    st.session_state.user_skills[user_id] = skills_interests.get('skills', [])
    
    # Save interests
    st.session_state.user_interests[user_id] = skills_interests.get('interests', [])
    
    return user_id

def save_payment(user_id, amount, mpesa_code, status, checkout_request_id=None):
    """Save payment information to session state"""
    payment_id = f"payment_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    st.session_state.payments[payment_id] = {
        'user_id': user_id,
        'amount': amount,
        'mpesa_code': mpesa_code,
        'checkout_request_id': checkout_request_id,
        'status': status,
        'created_at': datetime.now().isoformat()
    }

def save_career_results(user_id, recommendations):
    """Save career recommendations to session state"""
    result_id = f"result_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    st.session_state.career_results[result_id] = {
        'user_id': user_id,
        'recommendations': recommendations,
        'generated_at': datetime.now().isoformat()
    }

def check_payment_status(user_id):
    """Check if user has completed payment"""
    for payment_id, payment in st.session_state.payments.items():
        if payment['user_id'] == user_id and payment['status'] == 'completed':
            return True
    return False

def get_user_data(user_id):
    """Get user data by ID from session state"""
    user_id = int(user_id)  # Ensure it's integer for consistency
    
    if user_id not in st.session_state.users:
        return None
    
    return {
        'user_info': {
            'id': user_id,
            'name': st.session_state.users[user_id]['name'],
            'phone': st.session_state.users[user_id]['phone'],
            'email': st.session_state.users[user_id]['email'],
            'created_at': st.session_state.users[user_id]['created_at']
        },
        'subjects': st.session_state.user_subjects.get(user_id, {}),
        'skills': st.session_state.user_skills.get(user_id, []),
        'interests': st.session_state.user_interests.get(user_id, [])
    }

def get_payment_history(user_id):
    """Get payment history for a user from session state"""
    user_id = int(user_id)
    payment_list = []
    
    for payment_id, payment in st.session_state.payments.items():
        if payment['user_id'] == user_id:
            payment_list.append({
                'id': payment_id,
                'user_id': payment['user_id'],
                'amount': payment['amount'],
                'mpesa_code': payment['mpesa_code'],
                'checkout_request_id': payment['checkout_request_id'],
                'status': payment['status'],
                'created_at': payment['created_at']
            })
    
    # Sort by creation date (newest first)
    payment_list.sort(key=lambda x: x['created_at'], reverse=True)
    return payment_list

def get_career_results(user_id):
    """Get career results for a user from session state"""
    user_id = int(user_id)
    latest_result = None
    
    for result_id, result in st.session_state.career_results.items():
        if result['user_id'] == user_id:
            if latest_result is None or result['generated_at'] > latest_result['generated_at']:
                latest_result = result
    
    return latest_result

def cleanup_old_data(days_old=30):
    """Clean up data older than specified days (for maintenance) - Not needed for session state"""
    # Session state is temporary and clears when app restarts
    # No cleanup needed for demo purposes
    return 0

# Additional helper functions for session state management
def get_all_users():
    """Get all users from session state (for debugging)"""
    return st.session_state.users

def get_all_payments():
    """Get all payments from session state (for debugging)"""
    return st.session_state.payments

def clear_all_data():
    """Clear all data from session state (for testing)"""
    st.session_state.users = {}
    st.session_state.user_subjects = {}
    st.session_state.user_skills = {}
    st.session_state.user_interests = {}
    st.session_state.payments = {}
    st.session_state.career_results = {}
    st.session_state.user_counter = 0