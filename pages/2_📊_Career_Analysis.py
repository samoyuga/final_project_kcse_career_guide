import streamlit as st
import pandas as pd
from utils.database import init_db, save_user_data
from utils.career_engine import CareerEngine

def main():
    st.set_page_config(
        page_title="KCSE Career Guide - Analysis",
        page_icon="📊",
        layout="wide"
    )
    
    # Initialize database and career engine
    init_db()
    career_engine = CareerEngine()
    
    st.title("📚 KCSE Subject & Skills Analysis")
    st.markdown("### Enter your KCSE results and personal attributes for personalized career guidance")
    
    # Main input form
    with st.form("career_analysis_form"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.header("📖 KCSE Subjects & Grades")
            subjects_grades = get_subject_grades()
            
            st.header("🎯 Skills & Interests")
            skills_interests = get_skills_interests()
        
        with col2:
            st.header("👤 Student Information")
            student_info = get_student_info()
            
            st.markdown("---")
            st.subheader("📋 Form Validation")
            st.markdown("""
            **Requirements:**
            - ✅ 7-9 subjects total
            - ✅ Math, English, Kiswahili
            - ✅ 2+ Sciences
            - ✅ 1+ Humanity
            - ✅ Skills selected
            - ✅ Interests selected
            """)
        
        # Submit button
        submitted = st.form_submit_button("🚀 Generate Career Report", type="primary", width='stretch')
        
        if submitted:
            if validate_inputs(subjects_grades, skills_interests, student_info):
                # Save data and move to payment
                user_id = save_user_data(student_info, subjects_grades, skills_interests)
                st.session_state.user_id = user_id
                st.session_state.student_info = student_info
                st.session_state.subjects_grades = subjects_grades
                st.session_state.skills_interests = skills_interests
                
                st.success("✅ Data saved successfully! Proceeding to payment...")
                st.switch_page("pages/3_💳_Payment.py")
            else:
                st.error("❌ Please fix the errors above before proceeding.")

def get_subject_grades():
    """Get KCSE subjects and grades from user"""
    subjects = {}
    
    st.subheader("Mandatory Subjects")
    col1, col2, col3 = st.columns(3)
    with col1:
        subjects['Mathematics'] = st.selectbox("Mathematics*", ["Select Grade", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
    with col2:
        subjects['English'] = st.selectbox("English*", ["Select Grade", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
    with col3:
        subjects['Kiswahili'] = st.selectbox("Kiswahili*", ["Select Grade", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
    
    st.subheader("Science Subjects (Choose at least 2)")
    sci_col1, sci_col2, sci_col3 = st.columns(3)
    with sci_col1:
        subjects['Biology'] = st.selectbox("Biology", ["Not Taken", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
    with sci_col2:
        subjects['Chemistry'] = st.selectbox("Chemistry", ["Not Taken", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
    with sci_col3:
        subjects['Physics'] = st.selectbox("Physics", ["Not Taken", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
    
    st.subheader("Humanity Subjects (Choose at least 1)")
    hum_col1, hum_col2, hum_col3 = st.columns(3)
    with hum_col1:
        subjects['History'] = st.selectbox("History", ["Not Taken", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
    with hum_col2:
        subjects['Geography'] = st.selectbox("Geography", ["Not Taken", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
    with hum_col3:
        subjects['Religious Education'] = st.selectbox("Religious Education", ["Not Taken", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
    
    st.subheader("Technical & Other Subjects (Optional)")
    tech_col1, tech_col2 = st.columns(2)
    with tech_col1:
        subjects['Computer Studies'] = st.selectbox("Computer Studies", ["Not Taken", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
        subjects['Agriculture'] = st.selectbox("Agriculture", ["Not Taken", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
    with tech_col2:
        subjects['Business Studies'] = st.selectbox("Business Studies", ["Not Taken", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
        subjects['Home Science'] = st.selectbox("Home Science", ["Not Taken", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
    
    return subjects

def get_skills_interests():
    """Get skills and interests from user"""
    skills_interests = {}
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🛠️ Your Skills")
        skills = st.multiselect(
            "Select your strongest skills:",
            [
                "Problem Solving", "Critical Thinking", "Communication", "Leadership", 
                "Creativity", "Teamwork", "Analytical Thinking", "Research", 
                "Technical Skills", "Writing", "Public Speaking", "Organization",
                "Time Management", "Adaptability", "Attention to Detail"
            ],
            help="Choose skills that best describe you"
        )
        skills_interests['skills'] = skills
    
    with col2:
        st.subheader("❤️ Your Interests")
        interests = st.multiselect(
            "What are you passionate about?",
            [
                "Technology", "Medicine", "Engineering", "Business", "Arts", 
                "Sciences", "Education", "Agriculture", "Law", "Environment",
                "Politics", "Sports", "Music", "Writing", "Research",
                "Community Service", "Entrepreneurship", "Design", "Mathematics"
            ],
            help="Select areas that genuinely interest you"
        )
        skills_interests['interests'] = interests
    
    return skills_interests

def get_student_info():
    """Get student personal information"""
    student_info = {}
    
    st.subheader("Personal Details")
    student_info['name'] = st.text_input("Full Name*", placeholder="Enter your full name")
    student_info['phone'] = st.text_input("Phone Number*", placeholder="07XXXXXXXX", value="0723349693")
    student_info['email'] = st.text_input("Email Address", placeholder="your.email@example.com")
    
    return student_info

def validate_inputs(subjects_grades, skills_interests, student_info):
    """Validate all user inputs"""
    errors = []
    
    # Check mandatory subjects
    mandatory_subjects = ['Mathematics', 'English', 'Kiswahili']
    for subject in mandatory_subjects:
        if subjects_grades[subject] == "Select Grade":
            errors.append(f"❌ {subject} is a mandatory subject!")
    
    # Check sciences (at least 2)
    science_subjects = ['Biology', 'Chemistry', 'Physics']
    sciences_taken = [sub for sub in science_subjects if subjects_grades[sub] != "Not Taken"]
    if len(sciences_taken) < 2:
        errors.append("❌ You must select at least 2 Science subjects!")
    
    # Check humanities (at least 1)
    humanity_subjects = ['History', 'Geography', 'Religious Education']
    humanities_taken = [sub for sub in humanity_subjects if subjects_grades[sub] != "Not Taken"]
    if len(humanities_taken) < 1:
        errors.append("❌ You must select at least 1 Humanity subject!")
    
    # Check total subjects (7-9)
    all_subjects_taken = [sub for sub, grade in subjects_grades.items() if grade not in ["Not Taken", "Select Grade"]]
    if len(all_subjects_taken) < 7:
        errors.append("❌ You must have at least 7 subjects!")
    if len(all_subjects_taken) > 9:
        errors.append("❌ You can only have maximum 9 subjects!")
    
    # Check skills and interests
    if len(skills_interests['skills']) == 0:
        errors.append("❌ Please select at least one skill!")
    if len(skills_interests['interests']) == 0:
        errors.append("❌ Please select at least one interest!")
    
    # Check student info
    if not student_info['name'] or not student_info['name'].strip():
        errors.append("❌ Please enter your full name!")
    if not student_info['phone'] or not student_info['phone'].strip():
        errors.append("❌ Please enter your phone number!")
    elif len(student_info['phone']) < 10:
        errors.append("❌ Please enter a valid phone number!")
    
    # Display errors
    if errors:
        for error in errors:
            st.error(error)
        return False
    
    return True

if __name__ == "__main__":
    main()