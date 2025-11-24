import streamlit as st
import pandas as pd
import numpy as np
from utils.database import init_db, save_user_data, check_payment_status, save_payment, save_career_results
from utils.career_engine import CareerEngine
from utils.mpesa_integration import process_mpesa_payment
import json
import time
import os
from decouple import config

# Page configuration
st.set_page_config(
    page_title="KCSE Career Guide",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database and career engine
init_db()
career_engine = CareerEngine()

def get_subject_grades():
    """Get KCSE subjects and grades from user"""
    st.markdown("**Mandatory Subjects**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        math_grade = st.selectbox("Mathematics", ["Select Grade", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
    with col2:
        english_grade = st.selectbox("English", ["Select Grade", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
    with col3:
        kiswahili_grade = st.selectbox("Kiswahili", ["Select Grade", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
    
    st.markdown("**Science Subjects (Select at least 2)**")
    sci_col1, sci_col2, sci_col3 = st.columns(3)
    
    with sci_col1:
        biology = st.selectbox("Biology", ["Not Taken", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
    with sci_col2:
        chemistry = st.selectbox("Chemistry", ["Not Taken", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
    with sci_col3:
        physics = st.selectbox("Physics", ["Not Taken", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
    
    st.markdown("**Humanity Subjects (Select at least 1)**")
    hum_col1, hum_col2, hum_col3 = st.columns(3)
    
    with hum_col1:
        history = st.selectbox("History", ["Not Taken", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
    with hum_col2:
        geography = st.selectbox("Geography", ["Not Taken", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
    with hum_col3:
        religious_ed = st.selectbox("Religious Education", ["Not Taken", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
    
    st.markdown("**Technical Subjects (Optional)**")
    tech_col1, tech_col2 = st.columns(2)
    
    with tech_col1:
        computer_studies = st.selectbox("Computer Studies", ["Not Taken", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
        agriculture = st.selectbox("Agriculture", ["Not Taken", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
    with tech_col2:
        business_studies = st.selectbox("Business Studies", ["Not Taken", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
        home_science = st.selectbox("Home Science", ["Not Taken", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"], index=0)
    
    return {
        'Mathematics': math_grade,
        'English': english_grade,
        'Kiswahili': kiswahili_grade,
        'Biology': biology,
        'Chemistry': chemistry,
        'Physics': physics,
        'History': history,
        'Geography': geography,
        'Religious Education': religious_ed,
        'Computer Studies': computer_studies,
        'Agriculture': agriculture,
        'Business Studies': business_studies,
        'Home Science': home_science
    }

def get_skills_interests():
    """Get skills and interests from user"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🛠️ Skills")
        skills = st.multiselect(
            "Select your strongest skills:",
            ["Problem Solving", "Critical Thinking", "Communication", "Leadership", 
             "Creativity", "Teamwork", "Analytical Thinking", "Research", 
             "Technical Skills", "Writing", "Public Speaking", "Organization",
             "Time Management", "Adaptability", "Attention to Detail"]
        )
    
    with col2:
        st.subheader("❤️ Interests")
        interests = st.multiselect(
            "What are you passionate about?",
            ["Technology", "Medicine", "Engineering", "Business", "Arts", 
             "Sciences", "Education", "Agriculture", "Law", "Environment",
             "Politics", "Sports", "Music", "Writing", "Research",
             "Community Service", "Entrepreneurship", "Design", "Mathematics"]
        )
    
    return {
        'skills': skills,
        'interests': interests
    }

def get_student_info():
    """Get student personal information"""
    name = st.text_input("Full Name*", placeholder="Enter your full name")
    phone = st.text_input("Phone Number* (for M-Pesa)", placeholder="07XXXXXXXX", value="0723349693")
    email = st.text_input("Email Address", placeholder="your.email@example.com")
    
    return {
        'name': name,
        'phone': phone,
        'email': email
    }

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

def process_career_analysis(subjects_grades, skills_interests, student_info):
    """Process career analysis after payment"""
    try:
        # Save user data
        user_id = save_user_data(student_info, subjects_grades, skills_interests)
        
        # Process payment
        st.header("💳 M-Pesa Payment")
        
        # Display payment summary
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Payment Summary")
            st.write(f"**Name:** {student_info['name']}")
            st.write(f"**Phone:** {student_info['phone']}")
            st.write(f"**Amount:** KES 1")
            st.write(f"**Service:** Career Guidance Report")
        
        with col2:
            st.subheader("Next Steps")
            st.write("1. Click 'Proceed with Payment' below")
            st.write("2. Check your phone for M-Pesa prompt")
            st.write("3. Enter your M-Pesa PIN")
            st.write("4. Wait for confirmation")
        
        # Payment confirmation
        if st.button("✅ Proceed with M-Pesa Payment", type="primary", width='stretch'):
            with st.spinner("Initiating M-Pesa payment..."):
                payment_success = process_mpesa_payment(student_info['phone'], 1, user_id)
            
            if payment_success:
                # Save payment record
                save_payment(user_id, 1, f"CAREER_{user_id}", "completed")
                
                # Generate career recommendations
                with st.spinner("🎯 Analyzing your profile and generating career recommendations..."):
                    time.sleep(2)  # Simulate processing time
                    recommendations = career_engine.generate_recommendations(
                        subjects_grades, skills_interests
                    )
                
                # Save results
                save_career_results(user_id, recommendations)
                
                # Store in session state for results page
                st.session_state.user_id = user_id
                st.session_state.student_info = student_info
                st.session_state.subjects_grades = subjects_grades
                st.session_state.skills_interests = skills_interests
                st.session_state.recommendations = recommendations
                st.session_state.payment_completed = True
                
                # Display results immediately
                display_career_report(recommendations, subjects_grades, skills_interests, student_info)
                
            else:
                st.error("❌ Payment failed. Please try again or contact support.")
                st.info("💡 **Troubleshooting Tips:**")
                st.write("- Ensure your phone number is correct and has M-Pesa")
                st.write("- Check your mobile data connection")
                st.write("- Ensure you have sufficient M-Pesa balance")
                st.write("- If issues persist, try again after 5 minutes")
    
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.info("Please try again or contact support if the issue persists.")

def display_career_report(recommendations, subjects_grades, skills_interests, student_info):
    """Display the career analysis report"""
    st.header("📊 Your Personalized Career Report")
    
    # Overall suitability
    st.subheader("🎯 Career Match Overview")
    
    if not recommendations['top_careers']:
        st.warning("No career matches found based on your current profile. Please try adjusting your subject selections or skills.")
        return
    
    for career in recommendations['top_careers']:
        with st.expander(f"**{career['career']}** - {career['match_score']}% Match | *{career['cluster']}*", expanded=True):
            st.write(f"**Description:** {career['description']}")
            st.write(f"**Why it matches you:** {career['reasoning']}")
            
            # Match scores
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Subject Match", f"{career['subject_match']}%")
            with col2:
                st.metric("Skills Match", f"{career['skills_match']}%")
            with col3:
                st.metric("Interests Match", f"{career['interests_match']}%")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**📚 Recommended University Courses:**")
                for course in career['recommended_courses']:
                    st.write(f"- {course}")
            with col2:
                st.write("**🏛️ Kenyan Universities:**")
                for uni in career['universities'][:3]:  # Show top 3
                    st.write(f"- {uni}")
    
    # Subject analysis
    st.subheader("📈 Subject Performance Analysis")
    subject_data = []
    for subject, grade in subjects_grades.items():
        if grade not in ["Not Taken", "Select Grade"]:
            subject_data.append({
                'Subject': subject,
                'Grade': grade,
                'Score': career_engine.grade_to_points(grade)
            })
    
    if subject_data:
        df = pd.DataFrame(subject_data)
        st.dataframe(df, width='stretch')
    
    # Skills match
    st.subheader("🛠️ Skills & Interests Alignment")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Your Strongest Skills:**")
        for skill in skills_interests['skills']:
            st.write(f"✅ {skill}")
    
    with col2:
        st.write("**Your Key Interests:**")
        for interest in skills_interests['interests']:
            st.write(f"❤️ {interest}")
    
    # Download report
    st.subheader("📥 Download Report")
    if st.button("Download Career Report (TXT)", type="secondary"):
        download_report(recommendations, student_info, subjects_grades, skills_interests)

def download_report(recommendations, student_info, subjects_grades, skills_interests):
    """Generate and download report"""
    try:
        report_content = generate_report_content(recommendations, student_info, subjects_grades, skills_interests)
        
        st.download_button(
            label="📥 Download Report as TXT",
            data=report_content,
            file_name=f"career_report_{student_info.get('name', 'student')}.txt",
            mime="text/plain",
        )
        
    except Exception as e:
        st.error(f"❌ Error generating report: {str(e)}")

def generate_report_content(recommendations, student_info, subjects_grades, skills_interests):
    """Generate comprehensive report content"""
    report = []
    
    # Header
    report.append("=" * 60)
    report.append("           KCSE CAREER GUIDANCE REPORT")
    report.append("=" * 60)
    report.append(f"Student: {student_info.get('name', 'N/A')}")
    report.append(f"Phone: {student_info.get('phone', 'N/A')}")
    report.append(f"Email: {student_info.get('email', 'N/A')}")
    report.append(f"Report Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Executive Summary
    report.append("EXECUTIVE SUMMARY")
    report.append("-" * 40)
    if recommendations['top_careers']:
        top_career = recommendations['top_careers'][0]
        report.append(f"Primary Recommendation: {top_career['career']} ({top_career['match_score']}% match)")
        report.append(f"Total Suitable Careers: {len(recommendations['all_careers'])}")
        report.append("")
    
    # Top Recommendations
    report.append("TOP CAREER RECOMMENDATIONS")
    report.append("-" * 40)
    for i, career in enumerate(recommendations['top_careers']):
        report.append(f"{i+1}. {career['career']} ({career['cluster']})")
        report.append(f"   Overall Match: {career['match_score']}%")
        report.append(f"   Subject Match: {career['subject_match']}%")
        report.append(f"   Skills Match: {career['skills_match']}%")
        report.append(f"   Interests Match: {career['interests_match']}%")
        report.append(f"   Description: {career['description']}")
        report.append(f"   Reasoning: {career['reasoning']}")
        report.append("   Recommended Universities:")
        for uni in career['universities'][:3]:
            report.append(f"     - {uni}")
        report.append("   Suggested Courses:")
        for course in career['recommended_courses']:
            report.append(f"     - {course}")
        report.append("")
    
    # Subject Performance
    report.append("SUBJECT PERFORMANCE")
    report.append("-" * 40)
    taken_subjects = {sub: grade for sub, grade in subjects_grades.items() 
                     if grade not in ["Not Taken", "Select Grade"]}
    for subject, grade in taken_subjects.items():
        report.append(f"- {subject}: {grade}")
    report.append("")
    
    # Skills and Interests
    report.append("SKILLS AND INTERESTS PROFILE")
    report.append("-" * 40)
    report.append("Skills:")
    for skill in skills_interests.get('skills', []):
        report.append(f"- {skill}")
    report.append("")
    report.append("Interests:")
    for interest in skills_interests.get('interests', []):
        report.append(f"- {interest}")
    report.append("")
    
    report.append("=" * 60)
    report.append("End of Report")
    report.append("=" * 60)
    
    return "\n".join(report)

def main():
    # Custom CSS
    try:
        with open('assets/style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        st.markdown("""
        <style>
        .main { background-color: #f0f2f6; }
        .stButton>button { background-color: #4ECDC4; color: white; }
        </style>
        """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🎓 KCSE Career Guide")
    st.sidebar.markdown("""
    **How it works:**
    1. 📝 Enter your KCSE subjects and grades
    2. 🎯 Add your skills and interests
    3. 💳 Make payment (KES 1)
    4. 📊 Get your personalized career report
    """)
    
    # Add M-Pesa configuration info in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("💳 Payment Info")
    st.sidebar.markdown("""
    **M-Pesa Payment:**
    - Amount: KES 1
    - Paybill: 174379
    - Account: CAREER_[YourID]
    """)
    
    # Main app
    st.title("🎓 AI-Powered KCSE Career Guidance")
    st.markdown("### Discover your ideal career path based on your KCSE performance, skills, and interests")
    
    # User input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📚 KCSE Subjects & Grades")
        subjects_grades = get_subject_grades()
        
        st.header("🎯 Skills & Interests")
        skills_interests = get_skills_interests()
        
    with col2:
        st.header("👤 Student Info")
        student_info = get_student_info()
        
        if st.button("🚀 Generate Career Report", type="primary", width='stretch'):
            if validate_inputs(subjects_grades, skills_interests, student_info):
                process_career_analysis(subjects_grades, skills_interests, student_info)

if __name__ == "__main__":
    main()