import streamlit as st
import pandas as pd

def main():
    st.set_page_config(
        page_title="KCSE Career Guide - Home",
        page_icon="🏠",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 4px solid #4ECDC4;
    }
    .step-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header Section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="main-header">🎓 KCSE Career Guidance Tool</h1>', unsafe_allow_html=True)
        st.markdown("### *Discover Your Perfect Career Path*")
    
    # Hero Section
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h2>🤖 AI-Powered Career Matching</h2>
            <p>Our advanced AI analyzes your KCSE performance, skills, and interests to recommend the best career paths for you.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h2>📊 Personalized Reports</h2>
            <p>Get detailed career analysis with university recommendations, required grades, and career pathways.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h2>💳 Secure M-Pesa Payments</h2>
            <p>Pay conveniently via M-Pesa STK Push. Only KES 1 for your comprehensive career guidance report.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h2>🎯 Kenyan Education Focus</h2>
            <p>Specifically designed for the Kenyan education system with local university and career information.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # How It Works Section
    st.markdown("---")
    st.header("🚀 How It Works")
    
    steps_col1, steps_col2, steps_col3, steps_col4 = st.columns(4)
    
    with steps_col1:
        st.markdown("""
        <div class="step-card">
            <h3>1</h3>
            <h4>📝 Enter KCSE Grades</h4>
            <p>Input your KCSE subjects and grades with our validated form</p>
        </div>
        """, unsafe_allow_html=True)
    
    with steps_col2:
        st.markdown("""
        <div class="step-card">
            <h3>2</h3>
            <h4>🎯 Add Skills & Interests</h4>
            <p>Tell us about your strengths and passions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with steps_col3:
        st.markdown("""
        <div class="step-card">
            <h3>3</h3>
            <h4>💳 Make Payment</h4>
            <p>Pay KES 1 via M-Pesa STK Push</p>
        </div>
        """, unsafe_allow_html=True)
    
    with steps_col4:
        st.markdown("""
        <div class="step-card">
            <h3>4</h3>
            <h4>📊 Get Report</h4>
            <p>Receive your personalized career analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    # KCSE Information
    st.markdown("---")
    st.header("📚 About KCSE Subject Requirements")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Mandatory Subjects")
        mandatory_data = {
            'Subject': ['Mathematics', 'English', 'Kiswahili'],
            'Description': ['Core mathematics', 'Official language', 'National language']
        }
        st.dataframe(pd.DataFrame(mandatory_data), width='stretch')
    
    with col2:
        st.subheader("Subject Combinations")
        combo_data = {
            'Category': ['Sciences', 'Humanities', 'Technical', 'Total'],
            'Minimum Required': ['2 subjects', '1 subject', 'Optional', '7 subjects'],
            'Maximum Allowed': ['3 subjects', '3 subjects', '3 subjects', '9 subjects']
        }
        st.dataframe(pd.DataFrame(combo_data), width='stretch')
    
    # Call to Action
    st.markdown("---")
    st.header("🎯 Ready to Discover Your Career Path?")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Your Career Journey Now!", width='stretch', type="primary"):
            st.switch_page("pages/2_📊_Career_Analysis.py")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built with ❤️ for Kenyan Students | Secure & Confidential | M-Pesa Integrated</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()