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
                # Requirements
                st.subheader("📚 Requirements")
                if career['required_subjects']:
                    st.write("**Required Subjects:**")
                    for subject in career['required_subjects']:
                        required_grade = career['required_grades'].get(subject, 'C+')
                        user_grade = subjects_grades.get(subject, 'Not Taken')
                        status = "✅" if user_grade != "Not Taken" and user_grade != "Select Grade" else "❌"
                        st.write(f"{status} {subject}: {required_grade}+ (You: {user_grade})")
                
                # Skills alignment
                st.write("**Key Skills:**")
                user_skills = set(skills_interests.get('skills', []))
                career_skills = set(career.get('skills', []))
                for skill in career_skills:
                    status = "✅" if skill in user_skills else "⚪"
                    st.write(f"{status} {skill}")
            
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
        for subject, required_grade in top_career.get('required_grades', {}).items():
            user_grade = subjects_grades.get(subject, 'Not Taken')
            if user_grade in ["Not Taken", "Select Grade"]:
                weak_subjects.append(f"{subject} (not taken)")
            elif grade_to_points(user_grade) < grade_to_points(required_grade):
                weak_subjects.append(f"{subject} (needs {required_grade}+)")
        
        if weak_subjects:
            insights.append(f"To strengthen your candidacy for {top_career['career']}, consider: {', '.join(weak_subjects)}")
    
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