import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime

def main():
    st.set_page_config(
        page_title="KCSE Career Guide - Results",
        page_icon="📈",
        layout="wide"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .career-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #4ECDC4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .match-score {
        font-size: 2rem;
        font-weight: bold;
        color: #2c3e50;
    }
    .university-list {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .insight-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .requirement-met {
        color: #28a745;
        font-weight: bold;
    }
    .requirement-not-met {
        color: #dc3545;
        font-weight: bold;
    }
    .requirement-partial {
        color: #ffc107;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check if results exist
    if 'recommendations' not in st.session_state:
        st.error("❌ No career results found. Please complete the analysis and payment first.")
        if st.button("📝 Start Career Analysis"):
            st.switch_page("pages/2_📊_Career_Analysis.py")
        return
    
    recommendations = st.session_state.recommendations
    student_info = st.session_state.get('student_info', {})
    subjects_grades = st.session_state.get('subjects_grades', {})
    skills_interests = st.session_state.get('skills_interests', {})
    
    st.title("🎯 Your Career Guidance Report")
    st.markdown(f"### Personalized career analysis for **{student_info.get('name', 'Student')}**")
    
    # Header with download button
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("📥 Download Full Report", width='stretch'):
            download_report(recommendations, student_info, subjects_grades, skills_interests)
    
    st.markdown("---")
    
    # Executive Summary
    st.header("📊 Executive Summary")
    
    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    
    with summary_col1:
        st.metric(
            label="Top Career Match",
            value=f"{recommendations['top_careers'][0]['match_score']}%",
            delta="Primary Recommendation"
        )
    
    with summary_col2:
        st.metric(
            label="Career Options",
            value=len(recommendations['all_careers']),
            delta="Suitable Paths"
        )
    
    with summary_col3:
        st.metric(
            label="Subjects Analyzed",
            value=recommendations['user_profile']['subjects_count'],
            delta="KCSE Subjects"
        )
    
    with summary_col4:
        st.metric(
            label="Skills & Interests",
            value=recommendations['user_profile']['skills_count'] + recommendations['user_profile']['interests_count'],
            delta="Personal Attributes"
        )
    
    # Top Career Recommendations
    st.header("🎖️ Top Career Recommendations")
    
    for i, career in enumerate(recommendations['top_careers']):
        with st.expander(
            f"**#{i+1} {career['career']}** - **{career['match_score']}% Match** | *{career['cluster']}*",
            expanded=i == 0  # Expand first one by default
        ):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**📝 Description:** {career['description']}")
                st.markdown(f"**🎯 Why it matches you:** {career['reasoning']}")
                
                # Match breakdown
                st.subheader("Match Breakdown")
                match_data = {
                    'Category': ['Subject Match', 'Skills Match', 'Interests Match'],
                    'Score': [career['subject_match'], career['skills_match'], career['interests_match']]
                }
                match_df = pd.DataFrame(match_data)
                
                fig = px.bar(match_df, x='Category', y='Score', 
                           title=f"Match Analysis for {career['career']}",
                           color='Score', color_continuous_scale='Viridis',
                           range_y=[0, 100])
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, width='stretch')
                
            with col2:
                # Requirements - FIXED SECTION
                st.subheader("📚 Subject Requirements")
                display_subject_requirements(career, subjects_grades)
                
                # Skills alignment
                st.subheader("🛠️ Skills Alignment")
                user_skills = set(skills_interests.get('skills', []))
                career_skills = set(career.get('skills', []))
                
                if career_skills:
                    for skill in career_skills:
                        if skill in user_skills:
                            st.write(f"✅ **{skill}** - You have this skill")
                        else:
                            st.write(f"⚪ {skill} - Consider developing")
                else:
                    st.info("No specific skills requirements listed.")
            
            # University and Course Information
            st.subheader("🎓 Educational Pathway")
            
            uni_col1, uni_col2 = st.columns(2)
            
            with uni_col1:
                st.write("**Recommended Universities:**")
                for uni in career['universities'][:3]:  # Show top 3
                    st.write(f"🏛️ {uni}")
            
            with uni_col2:
                st.write("**Suggested Courses:**")
                for course in career['recommended_courses']:
                    st.write(f"📖 {course}")
    
    # All Career Options
    if len(recommendations['all_careers']) > 5:
        st.header("📋 All Suitable Career Options")
        
        # Create dataframe for all careers
        all_careers_data = []
        for career in recommendations['all_careers']:
            all_careers_data.append({
                'Career': career['career'],
                'Cluster': career['cluster'],
                'Overall Match': career['match_score'],
                'Subject Match': career['subject_match'],
                'Skills Match': career['skills_match'],
                'Interests Match': career['interests_match']
            })
        
        all_careers_df = pd.DataFrame(all_careers_data)
        st.dataframe(all_careers_df, width='stretch')
    
    # Subject Performance Analysis
    st.header("📈 Subject Performance Analysis")
    
    # Filter out "Not Taken" and "Select Grade" subjects
    taken_subjects = {sub: grade for sub, grade in subjects_grades.items() 
                     if grade not in ["Not Taken", "Select Grade"]}
    
    if taken_subjects:
        col1, col2 = st.columns(2)
        
        with col1:
            # Subject grades table
            st.subheader("Your KCSE Grades")
            subject_data = []
            for subject, grade in taken_subjects.items():
                subject_data.append({
                    'Subject': subject,
                    'Grade': grade,
                    'Points': grade_to_points(grade)
                })
            
            subject_df = pd.DataFrame(subject_data)
            st.dataframe(subject_df, width='stretch')
        
        with col2:
            # Subject distribution chart
            st.subheader("Grade Distribution")
            grade_counts = pd.Series([grade for grade in taken_subjects.values()]).value_counts()
            fig = px.pie(values=grade_counts.values, names=grade_counts.index,
                        title="Distribution of Your Grades")
            st.plotly_chart(fig, width='stretch')
    
    # Skills and Interests Analysis
    st.header("🛠️ Skills & Interests Profile")
    
    skills_col1, skills_col2 = st.columns(2)
    
    with skills_col1:
        st.subheader("Your Skills")
        skills = skills_interests.get('skills', [])
        if skills:
            skills_df = pd.DataFrame({'Skill': skills, 'Count': [1]*len(skills)})
            fig = px.bar(skills_df, x='Count', y='Skill', orientation='h',
                        title="Your Skills Profile", color='Count',
                        color_continuous_scale='Blues')
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("No skills selected")
    
    with skills_col2:
        st.subheader("Your Interests")
        interests = skills_interests.get('interests', [])
        if interests:
            interests_df = pd.DataFrame({'Interest': interests, 'Count': [1]*len(interests)})
            fig = px.bar(interests_df, x='Count', y='Interest', orientation='h',
                        title="Your Interests Profile", color='Count',
                        color_continuous_scale='Greens')
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("No interests selected")
    
    # Career Cluster Analysis
    st.header("🏗️ Career Clusters Analysis")
    
    # Group by cluster
    cluster_data = {}
    for career in recommendations['all_careers']:
        cluster = career['cluster']
        if cluster not in cluster_data:
            cluster_data[cluster] = []
        cluster_data[cluster].append(career['match_score'])
    
    cluster_stats = []
    for cluster, scores in cluster_data.items():
        cluster_stats.append({
            'Cluster': cluster,
            'Average Match': sum(scores) / len(scores),
            'Career Count': len(scores)
        })
    
    cluster_df = pd.DataFrame(cluster_stats)
    
    if not cluster_df.empty:
        fig = px.bar(cluster_df, x='Cluster', y='Average Match',
                    title="Average Match Score by Career Cluster",
                    color='Average Match', color_continuous_scale='Viridis')
        st.plotly_chart(fig, width='stretch')
    
    # Actionable Insights
    st.header("💡 Actionable Insights & Next Steps")
    
    insights = generate_insights(recommendations, subjects_grades, skills_interests)
    
    for i, insight in enumerate(insights):
        st.markdown(f"""
        <div class="insight-box">
            <h4>💡 Insight #{i+1}</h4>
            <p>{insight}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Next Steps
    st.header("🚀 Your Next Steps")
    
    steps_col1, steps_col2, steps_col3 = st.columns(3)
    
    with steps_col1:
        st.markdown("""
        ### 📚 Academic Preparation
        - Research university requirements
        - Identify subject prerequisites
        - Plan your academic pathway
        - Consider bridging courses if needed
        """)
    
    with steps_col2:
        st.markdown("""
        ### 🛠️ Skill Development
        - Identify skill gaps
        - Seek relevant experiences
        - Consider internships
        - Join related clubs/societies
        """)
    
    with steps_col3:
        st.markdown("""
        ### 🔍 Career Exploration
        - Shadow professionals
        - Attend career fairs
        - Research job markets
        - Network with alumni
        """)
    
    # Footer with navigation
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Start New Analysis", width='stretch'):
            # Clear session state and start over
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.switch_page("pages/1_🏠_Home.py")
    
    with col2:
        if st.button("📊 Back to Analysis", width='stretch'):
            st.switch_page("pages/2_📊_Career_Analysis.py")
    
    with col3:
        if st.button("📥 Download Report", width='stretch'):
            download_report(recommendations, student_info, subjects_grades, skills_interests)

def grade_to_points(grade):
    """Convert grade to points"""
    grade_points = {
        'A': 12, 'A-': 11, 'B+': 10, 'B': 9, 'B-': 8,
        'C+': 7, 'C': 6, 'C-': 5, 'D+': 4, 'D': 3, 'D-': 2, 'E': 1
    }
    return grade_points.get(grade, 0)

def get_cluster_requirements(cluster_name):
    """Get the specific 4 requirements for a cluster with exact subject groupings"""
    
    # Define subject groups
    GROUP_I = ['English', 'Kiswahili', 'Mathematics']
    GROUP_II = ['Biology', 'Physics', 'Chemistry']
    GROUP_III = ['History', 'Geography', 'CRE', 'IRE', 'HRE']
    GROUP_IV = ['Home Science', 'Art & Design', 'Agriculture', 'Woodwork', 'Metalwork', 
                'Building Construction', 'Power Mechanics', 'Electricity', 'Drawing & Design', 
                'Aviation', 'Computer Studies']
    GROUP_V = ['French', 'German', 'Arabic', 'Kenya Sign Language', 'Music', 'Business Studies']
    
    # Extract cluster ID from the cluster name
    cluster_id = None
    if "Cluster 1:" in cluster_name:
        cluster_id = 1
    elif "Cluster 2:" in cluster_name:
        cluster_id = 2
    elif "Cluster 3:" in cluster_name:
        cluster_id = 3
    elif "Cluster 4:" in cluster_name:
        cluster_id = 4
    elif "Cluster 5:" in cluster_name:
        cluster_id = 5
    elif "Cluster 6:" in cluster_name:
        cluster_id = 6
    elif "Cluster 7:" in cluster_name:
        cluster_id = 7
    elif "Cluster 8:" in cluster_name:
        cluster_id = 8
    elif "Cluster 9:" in cluster_name:
        cluster_id = 9
    elif "Cluster 10:" in cluster_name:
        cluster_id = 10
    elif "Cluster 11:" in cluster_name:
        cluster_id = 11
    elif "Cluster 12:" in cluster_name:
        cluster_id = 12
    elif "Cluster 13:" in cluster_name:
        cluster_id = 13
    elif "Cluster 14:" in cluster_name:
        cluster_id = 14
    elif "Cluster 15:" in cluster_name:
        cluster_id = 15
    elif "Cluster 16:" in cluster_name:
        cluster_id = 16
    elif "Cluster 17:" in cluster_name:
        cluster_id = 17
    elif "Cluster 18:" in cluster_name:
        cluster_id = 18
    elif "Cluster 19:" in cluster_name:
        cluster_id = 19
    elif "Cluster 20:" in cluster_name:
        cluster_id = 20
    
    # Return requirements based on cluster ID - ALL GRADES CORRECTED TO 'C+'
    requirements = {
        1: {  # LAW
            'English': {'subjects': ['English'], 'min_grade': 'B'},
            'Any Group II': {'subjects': GROUP_II, 'min_grade': 'C+'},
            'Any Group III': {'subjects': GROUP_III, 'min_grade': 'C+'},
            'Any Group III/IV/V': {'subjects': GROUP_III + GROUP_IV + GROUP_V, 'min_grade': 'C+'}
        },
        2: {  # BUSINESS & HOSPITALITY
            'Mathematics': {'subjects': ['Mathematics'], 'min_grade': 'C+'},
            'Any Group II': {'subjects': GROUP_II, 'min_grade': 'C+'},
            'Any Group III': {'subjects': GROUP_III, 'min_grade': 'C+'},
            'Any Group III/IV/V': {'subjects': GROUP_III + GROUP_IV + GROUP_V, 'min_grade': 'C+'}
        },
        3: {  # SOCIAL SCIENCES, MEDIA, ARTS
            'Group II/III 1': {'subjects': GROUP_II + GROUP_III, 'min_grade': 'C+'},
            'Group II/III 2': {'subjects': GROUP_II + GROUP_III, 'min_grade': 'C+'},
            'Group II/III 3': {'subjects': GROUP_II + GROUP_III, 'min_grade': 'C+'},
            'Any Other Subject': {'subjects': GROUP_II + GROUP_III + GROUP_IV + GROUP_V, 'min_grade': 'C+'}
        },
        4: {  # GEOSCIENCES
            'Mathematics': {'subjects': ['Mathematics'], 'min_grade': 'C+'},
            'Physics': {'subjects': ['Physics'], 'min_grade': 'C+'},
            'Biology/Chemistry/Geography': {'subjects': ['Biology', 'Chemistry', 'Geography'], 'min_grade': 'C'},
            'Any Group II/III/IV/V': {'subjects': GROUP_II + GROUP_III + GROUP_IV + GROUP_V, 'min_grade': 'C+'}
        },
        5: {  # ENGINEERING
            'Mathematics': {'subjects': ['Mathematics'], 'min_grade': 'C+'},
            'Physics': {'subjects': ['Physics'], 'min_grade': 'C+'},
            'Chemistry': {'subjects': ['Chemistry'], 'min_grade': 'C+'},
            'English/Kiswahili': {'subjects': ['English', 'Kiswahili'], 'min_grade': 'C+'}
        },
        6: {  # ARCHITECTURE & CONSTRUCTION
            'Mathematics': {'subjects': ['Mathematics'], 'min_grade': 'C+'},
            'Physics': {'subjects': ['Physics'], 'min_grade': 'C+'},
            'Any Group III': {'subjects': GROUP_III, 'min_grade': 'C+'},
            'English/Kiswahili': {'subjects': ['English', 'Kiswahili'], 'min_grade': 'C+'}
        },
        7: {  # COMPUTING & IT
            'Mathematics': {'subjects': ['Mathematics'], 'min_grade': 'C+'},
            'Physics': {'subjects': ['Physics'], 'min_grade': 'C+'},
            'Any Group II/III': {'subjects': GROUP_II + GROUP_III, 'min_grade': 'C+'},
            'English/Kiswahili': {'subjects': ['English', 'Kiswahili'], 'min_grade': 'C'}
        },
        8: {  # AGRIBUSINESS
            'Mathematics': {'subjects': ['Mathematics'], 'min_grade': 'C'},
            'Biology': {'subjects': ['Biology'], 'min_grade': 'C'},
            'Chemistry/Physics/Agriculture': {'subjects': ['Chemistry', 'Physics', 'Agriculture'], 'min_grade': 'C'},
            'Any Group II/III/IV/V': {'subjects': GROUP_II + GROUP_III + GROUP_IV + GROUP_V, 'min_grade': 'C+'}
        },
        9: {  # GENERAL SCIENCES
            'Mathematics': {'subjects': ['Mathematics'], 'min_grade': 'C'},
            'Any Group II': {'subjects': GROUP_II, 'min_grade': 'C'},
            'Any Group III': {'subjects': GROUP_III, 'min_grade': 'C'},
            'Any Group II/III/IV/V': {'subjects': GROUP_II + GROUP_III + GROUP_IV + GROUP_V, 'min_grade': 'C+'}
        },
        10: {  # ACTUARIAL, MATHEMATICS, ECONOMICS
            'Mathematics': {'subjects': ['Mathematics'], 'min_grade': 'C+'},
            'Any Group II': {'subjects': GROUP_II, 'min_grade': 'C+'},
            'Any Group III': {'subjects': GROUP_III, 'min_grade': 'C+'},
            'English/Kiswahili': {'subjects': ['English', 'Kiswahili'], 'min_grade': 'C+'}
        },
        11: {  # DESIGN
            'Chemistry': {'subjects': ['Chemistry'], 'min_grade': 'C'},
            'Mathematics/Physics': {'subjects': ['Mathematics', 'Physics'], 'min_grade': 'C'},
            'Biology/Home Science': {'subjects': ['Biology', 'Home Science'], 'min_grade': 'C'},
            'Any Group III/IV/V': {'subjects': GROUP_III + GROUP_IV + GROUP_V, 'min_grade': 'C+'}
        },
        12: {  # SPORTS SCIENCE
            'Biology/General Science': {'subjects': ['Biology', 'General Science'], 'min_grade': 'C+'},
            'Mathematics': {'subjects': ['Mathematics'], 'min_grade': 'C+'},
            'Any Group II/III': {'subjects': GROUP_II + GROUP_III, 'min_grade': 'C+'},
            'Any Group II/III/IV/V': {'subjects': GROUP_II + GROUP_III + GROUP_IV + GROUP_V, 'min_grade': 'C+'}
        },
        13: {  # MEDICINE & HEALTH
            'Biology': {'subjects': ['Biology'], 'min_grade': 'B'},
            'Chemistry': {'subjects': ['Chemistry'], 'min_grade': 'B'},
            'Mathematics/Physics': {'subjects': ['Mathematics', 'Physics'], 'min_grade': 'B'},
            'English/Kiswahili': {'subjects': ['English', 'Kiswahili'], 'min_grade': 'B'}
        },
        14: {  # HISTORY & ARCHAEOLOGY
            'History': {'subjects': ['History'], 'min_grade': 'C+'},
            'English/Kiswahili': {'subjects': ['English', 'Kiswahili'], 'min_grade': 'C+'},
            'Mathematics/Any Group II': {'subjects': ['Mathematics'] + GROUP_II, 'min_grade': 'C+'},
            'Any Group II/IV/V': {'subjects': GROUP_II + GROUP_IV + GROUP_V, 'min_grade': 'C+'}
        },
        15: {  # AGRICULTURE & ENVIRONMENT
            'Biology': {'subjects': ['Biology'], 'min_grade': 'C+'},
            'Chemistry': {'subjects': ['Chemistry'], 'min_grade': 'C+'},
            'Mathematics/Physics/Geography': {'subjects': ['Mathematics', 'Physics', 'Geography'], 'min_grade': 'C+'},
            'English/Kiswahili': {'subjects': ['English', 'Kiswahili'], 'min_grade': 'C+'}
        },
        16: {  # GEOGRAPHY
            'Geography': {'subjects': ['Geography'], 'min_grade': 'C+'},
            'Mathematics': {'subjects': ['Mathematics'], 'min_grade': 'C+'},
            'Any Group II': {'subjects': GROUP_II, 'min_grade': 'C+'},
            'Any Group II/III/IV/V': {'subjects': GROUP_II + GROUP_III + GROUP_IV + GROUP_V, 'min_grade': 'C+'}
        },
        17: {  # LANGUAGES
            'French/German': {'subjects': ['French', 'German'], 'min_grade': 'C+'},
            'English/Kiswahili': {'subjects': ['English', 'Kiswahili'], 'min_grade': 'C+'},
            'Any Group II/III': {'subjects': GROUP_II + GROUP_III, 'min_grade': 'C+'},
            'Any Group II/III/IV/V': {'subjects': GROUP_II + GROUP_III + GROUP_IV + GROUP_V, 'min_grade': 'C+'}
        },
        18: {  # MUSIC
            'Music': {'subjects': ['Music'], 'min_grade': 'C+'},
            'English/Kiswahili': {'subjects': ['English', 'Kiswahili'], 'min_grade': 'C+'},
            'Any Group II/III': {'subjects': GROUP_II + GROUP_III, 'min_grade': 'C+'},
            'Any Group II/III/IV/V': {'subjects': GROUP_II + GROUP_III + GROUP_IV + GROUP_V, 'min_grade': 'C+'}
        },
        19: {  # EDUCATION
            'Teaching Subject 1': {'subjects': GROUP_I + GROUP_III + ['Social Studies', 'Home Science', 'Art & Design', 'Computer Studies', 'Music', 'French', 'German'], 'min_grade': 'C+'},
            'Teaching Subject 2': {'subjects': GROUP_I + GROUP_III + ['Social Studies', 'Home Science', 'Art & Design', 'Computer Studies', 'Music', 'French', 'German'], 'min_grade': 'C+'},
            'Science Subject': {'subjects': GROUP_II + ['Business Studies', 'Agriculture'], 'min_grade': 'C+'},
            'Additional Subject': {'subjects': GROUP_II + ['Business Studies', 'Agriculture'], 'min_grade': 'C+'}
        },
        20: {  # RELIGIOUS STUDIES
            'CRE/IRE/HRE': {'subjects': ['CRE', 'IRE', 'HRE'], 'min_grade': 'C+'},
            'English/Kiswahili': {'subjects': ['English', 'Kiswahili'], 'min_grade': 'C'},
            'Any Group III': {'subjects': GROUP_III, 'min_grade': 'C+'},
            'Any Group II/IV/V': {'subjects': GROUP_II + GROUP_IV + GROUP_V, 'min_grade': 'C+'}
        }
    }
    
    return requirements.get(cluster_id, {
        'Mathematics': {'subjects': ['Mathematics'], 'min_grade': 'C+'},
        'English': {'subjects': ['English'], 'min_grade': 'C+'},
        'Any Science': {'subjects': GROUP_II, 'min_grade': 'C+'},
        'Any Humanities': {'subjects': GROUP_III, 'min_grade': 'C+'}
    })

def check_group_requirement(group_requirement, subjects_grades):
    """Check if user meets 'Any Group' requirements with exact subject groupings"""
    
    # Define exact subject groups
    GROUP_I = ['English', 'Kiswahili', 'Mathematics']
    GROUP_II = ['Biology', 'Physics', 'Chemistry']
    GROUP_III = ['History', 'Geography', 'CRE', 'IRE', 'HRE']
    GROUP_IV = ['Home Science', 'Art & Design', 'Agriculture', 'Woodwork', 'Metalwork', 
                'Building Construction', 'Power Mechanics', 'Electricity', 'Drawing & Design', 
                'Aviation', 'Computer Studies']
    GROUP_V = ['French', 'German', 'Arabic', 'Kenya Sign Language', 'Music', 'Business Studies']
    
    # Get user's taken subjects with decent grades (C+ and above)
    taken_subjects = {sub: grade for sub, grade in subjects_grades.items() 
                     if grade not in ["Not Taken", "Select Grade"] and grade_to_points(grade) >= grade_to_points('C+')}
    
    # Check group requirements
    if 'Group I' in group_requirement:
        return any(subject in taken_subjects for subject in GROUP_I)
    elif 'Group II' in group_requirement:
        return any(subject in taken_subjects for subject in GROUP_II)
    elif 'Group III' in group_requirement:
        return any(subject in taken_subjects for subject in GROUP_III)
    elif 'Group IV' in group_requirement:
        return any(subject in taken_subjects for subject in GROUP_IV)
    elif 'Group V' in group_requirement:
        return any(subject in taken_subjects for subject in GROUP_V)
    elif 'Group II/III' in group_requirement:
        return any(subject in taken_subjects for subject in GROUP_II + GROUP_III)
    elif 'Group III/IV/V' in group_requirement:
        return any(subject in taken_subjects for subject in GROUP_III + GROUP_IV + GROUP_V)
    elif 'Group II/III/IV/V' in group_requirement:
        return any(subject in taken_subjects for subject in GROUP_II + GROUP_III + GROUP_IV + GROUP_V)
    
    return False

def display_subject_requirements(career, subjects_grades):
    """Display ONLY the 4 specific required subjects for this career"""
    
    # Get the cluster-specific requirements (maximum 4 subjects)
    cluster_requirements = get_cluster_requirements(career['cluster'])
    
    if not cluster_requirements:
        st.info("Specific subject requirements not available for this career.")
        return
    
    # Track used subjects to avoid repetition
    used_subjects = set()
    requirements_met = 0
    total_requirements = len(cluster_requirements)
    
    st.write("**Required Subjects:**")
    
    for req_name, requirement in cluster_requirements.items():
        subject_options = requirement['subjects']
        required_grade = requirement['min_grade']
        
        # Find the best matching subject (highest grade) that hasn't been used yet
        best_subject = None
        best_grade = None
        best_points = -1
        
        for subject in subject_options:
            # Skip if subject already used
            if subject in used_subjects:
                continue
                
            user_grade = subjects_grades.get(subject, 'Not Taken')
            
            if user_grade not in ["Not Taken", "Select Grade"]:
                user_points = grade_to_points(user_grade)
                required_points = grade_to_points(required_grade)
                
                # Track the subject with the highest grade that meets requirement
                if user_points >= required_points and user_points > best_points:
                    best_subject = subject
                    best_grade = user_grade
                    best_points = user_points
                elif user_points > best_points:  # Track highest grade even if not meeting requirement
                    best_subject = subject
                    best_grade = user_grade
                    best_points = user_points
        
        # Check if requirement is met
        requirement_met = False
        if best_subject and best_points >= grade_to_points(required_grade):
            requirement_met = True
            used_subjects.add(best_subject)
            requirements_met += 1
            status = "✅"
            status_class = "requirement-met"
            message = f"**{req_name}**: {best_subject}: {best_grade} (Required: {required_grade}+)"
        elif best_subject:
            # Subject available but grade not sufficient
            used_subjects.add(best_subject)
            status = "⚠️"
            status_class = "requirement-partial"
            message = f"**{req_name}**: {best_subject}: {best_grade} (Required: {required_grade}+)"
        else:
            # No suitable subject found
            status = "❌"
            status_class = "requirement-not-met"
            # Show a few sample subjects from the group
            sample_subjects = [s for s in subject_options if s not in used_subjects][:3]
            subject_list = ", ".join(sample_subjects) if sample_subjects else "No suitable subjects"
            message = f"**{req_name}**: {subject_list} (Required: {required_grade}+)"
        
        st.markdown(f'<span class="{status_class}">{status} {message}</span>', unsafe_allow_html=True)
    
    # Show overall requirement status
    st.markdown("---")
    if requirements_met == total_requirements:
        st.success(f"✅ **All {total_requirements} requirements met!**")
    elif requirements_met > 0:
        st.warning(f"⚠️ **{requirements_met} out of {total_requirements} requirements met**")
    else:
        st.error(f"❌ **None of the {total_requirements} requirements met**")

def generate_insights(recommendations, subjects_grades, skills_interests):
    """Generate personalized insights based on the analysis"""
    insights = []
    
    if not recommendations['top_careers']:
        insights.append("Based on your current profile, consider exploring a wider range of career options or focusing on improving specific subject areas to expand your opportunities.")
        return insights
    
    top_career = recommendations['top_careers'][0]
    
    # Overall match insight
    if top_career['match_score'] >= 85:
        insights.append(f"Excellent! Your profile shows strong alignment with {top_career['career']}. You have the right combination of academic strengths, skills, and interests for this career path.")
    elif top_career['match_score'] >= 70:
        insights.append(f"Good match! {top_career['career']} aligns well with your profile. Consider gaining more experience in this field to strengthen your position.")
    else:
        insights.append(f"While {top_career['career']} shows potential, there are areas for improvement. Focus on developing the required skills and meeting academic prerequisites.")
    
    # Subject-based insights
    if top_career['subject_match'] < 70:
        weak_subjects = []
        for subject in top_career.get('required_subjects', []):
            required_grade = top_career['required_grades'].get(subject, 'C+')
            user_grade = subjects_grades.get(subject, 'Not Taken')
            
            if user_grade in ["Not Taken", "Select Grade"]:
                weak_subjects.append(f"{subject} (not taken)")
            elif grade_to_points(user_grade) < grade_to_points(required_grade):
                weak_subjects.append(f"{subject} (needs {required_grade}+, you have {user_grade})")
        
        if weak_subjects:
            insights.append(f"To strengthen your candidacy for {top_career['career']}, focus on: {', '.join(weak_subjects[:3])}")
    
    # Skills insights
    user_skills = set(skills_interests.get('skills', []))
    career_skills = set(top_career.get('skills', []))
    missing_skills = career_skills - user_skills
    
    if missing_skills and len(missing_skills) > 0:
        insights.append(f"Develop these key skills for {top_career['career']}: {', '.join(list(missing_skills)[:3])}")
    
    # Cluster diversity insight
    clusters = set(career['cluster'] for career in recommendations['top_careers'][:3])
    if len(clusters) >= 2:
        insights.append(f"Your profile shows versatility across different fields ({', '.join(clusters)}), giving you multiple career pathway options.")
    
    # Strength identification
    strongest_match = max(recommendations['top_careers'], 
                         key=lambda x: x['subject_match'] + x['skills_match'] + x['interests_match'])
    insights.append(f"Your strongest alignment factors are in {strongest_match['cluster']} careers, particularly where academic performance and personal attributes converge.")
    
    return insights

def download_report(recommendations, student_info, subjects_grades, skills_interests):
    """Generate and download report"""
    try:
        # Create report content
        report_content = generate_report_content(recommendations, student_info, subjects_grades, skills_interests)
        
        # For now, we'll create a text file. In production, you might want to generate PDF
        st.download_button(
            label="📥 Download Report as TXT",
            data=report_content,
            file_name=f"career_report_{student_info.get('name', 'student')}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            key="download_txt"
        )
        
        st.success("✅ Report generated successfully! Click the download button above.")
        
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
    report.append(f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Executive Summary
    report.append("EXECUTIVE SUMMARY")
    report.append("-" * 40)
    if recommendations['top_careers']:
        top_career = recommendations['top_careers'][0]
        report.append(f"Primary Recommendation: {top_career['career']} ({top_career['match_score']}% match)")
        report.append(f"Total Suitable Careers: {len(recommendations['all_careers'])}")
        report.append(f"Subjects Analyzed: {recommendations['user_profile']['subjects_count']}")
        report.append("")
    
    # Top Recommendations
    report.append("TOP CAREER RECOMMENDATIONS")
    report.append("-" * 40)
    for i, career in enumerate(recommendations['top_careers'][:5]):
        report.append(f"{i+1}. {career['career']} ({career['cluster']})")
        report.append(f"   Overall Match: {career['match_score']}%")
        report.append(f"   Subject Match: {career['subject_match']}%")
        report.append(f"   Skills Match: {career['skills_match']}%")
        report.append(f"   Interests Match: {career['interests_match']}%")
        report.append(f"   Description: {career['description']}")
        report.append(f"   Reasoning: {career['reasoning']}")
        
        # Subject Requirements
        report.append("   Subject Requirements:")
        for subject in career['required_subjects']:
            required_grade = career['required_grades'].get(subject, 'C+')
            user_grade = subjects_grades.get(subject, 'Not Taken')
            status = "MET" if user_grade not in ["Not Taken", "Select Grade"] and grade_to_points(user_grade) >= grade_to_points(required_grade) else "NOT MET"
            report.append(f"     - {subject}: Required {required_grade}+ (You: {user_grade}) [{status}]")
        
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
        report.append(f"- {subject}: {grade} ({grade_to_points(grade)} points)")
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
    
    # Insights and Recommendations
    report.append("ACTIONABLE INSIGHTS")
    report.append("-" * 40)
    insights = generate_insights(recommendations, subjects_grades, skills_interests)
    for i, insight in enumerate(insights):
        report.append(f"{i+1}. {insight}")
    report.append("")
    
    # Next Steps
    report.append("NEXT STEPS")
    report.append("-" * 40)
    report.append("1. Research your top career recommendations in depth")
    report.append("2. Contact universities for specific admission requirements")
    report.append("3. Develop the identified skills through courses or experiences")
    report.append("4. Seek mentorship from professionals in your chosen field")
    report.append("5. Consider internships or job shadowing opportunities")
    report.append("")
    
    report.append("=" * 60)
    report.append("End of Report")
    report.append("=" * 60)
    
    return "\n".join(report)

if __name__ == "__main__":
    main()