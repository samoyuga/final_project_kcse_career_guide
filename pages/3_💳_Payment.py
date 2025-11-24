import streamlit as st
import time
from utils.database import save_payment, save_career_results
from utils.career_engine import CareerEngine
from utils.mpesa_integration import process_mpesa_payment

def main():
    st.set_page_config(
        page_title="KCSE Career Guide - Payment",
        page_icon="💳",
        layout="wide"
    )
    
    # Check if user data exists
    if 'user_id' not in st.session_state or 'subjects_grades' not in st.session_state:
        st.error("❌ Please complete the career analysis form first.")
        if st.button("📝 Go to Analysis Form"):
            st.switch_page("pages/2_📊_Career_Analysis.py")
        return
    
    st.title("💳 Payment & Report Generation")
    st.markdown("### Complete your payment to generate personalized career report")
    
    user_id = st.session_state.user_id
    student_info = st.session_state.student_info
    subjects_grades = st.session_state.subjects_grades
    skills_interests = st.session_state.skills_interests
    
    # Display summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Order Summary")
        st.write(f"**Name:** {student_info['name']}")
        st.write(f"**Phone:** {student_info['phone']}")
        st.write(f"**Email:** {student_info.get('email', 'Not provided')}")
        st.write(f"**Service:** AI Career Guidance Report")
        st.write(f"**Amount:** KES 1")
        
        st.markdown("---")
        st.subheader("📚 Subjects Summary")
        taken_subjects = {sub: grade for sub, grade in subjects_grades.items() if grade not in ["Not Taken", "Select Grade"]}
        for subject, grade in taken_subjects.items():
            st.write(f"• {subject}: {grade}")
    
    with col2:
        st.subheader("🎯 Skills & Interests")
        st.write("**Skills:**")
        for skill in skills_interests['skills']:
            st.write(f"• {skill}")
        
        st.write("**Interests:**")
        for interest in skills_interests['interests']:
            st.write(f"• {interest}")
        
        st.markdown("---")
        st.subheader("ℹ️ Payment Instructions")
        st.markdown("""
        1. Click **'Pay via M-Pesa'** button
        2. Check your phone for M-Pesa prompt
        3. Enter your M-Pesa PIN
        4. Wait for automatic confirmation
        5. Receive your career report instantly
        """)
    
    # Payment section
    st.markdown("---")
    st.header("🔐 Secure M-Pesa Payment")
    
    payment_col1, payment_col2 = st.columns([1, 1])
    
    with payment_col1:
        st.subheader("Payment Details")
        st.info("""
        **M-Pesa Payment Info:**
        - Amount: KES 1
        - PayBill: 174379
        - Account: CAREER_[YourID]
        - No extra charges
        """)
    
    with payment_col2:
        st.subheader("Initiate Payment")
        if st.button("💰 Pay via M-Pesa", type="primary", width='stretch'):
            with st.spinner("Initiating M-Pesa payment..."):
                # Process actual M-Pesa payment
                payment_success = process_mpesa_payment(
                    student_info['phone'], 
                    1, 
                    user_id
                )
            
            if payment_success:
                # Save payment record
                save_payment(user_id, 1, f"CAREER_{user_id}", "completed")
                
                # Generate career recommendations
                with st.spinner("🎯 Generating your personalized career report..."):
                    career_engine = CareerEngine()
                    recommendations = career_engine.generate_recommendations(
                        subjects_grades, skills_interests
                    )
                
                # Save results to database
                save_career_results(user_id, recommendations)
                
                # Store recommendations in session state
                st.session_state.recommendations = recommendations
                st.session_state.payment_completed = True
                
                st.success("✅ Payment confirmed! Your report is ready.")
                st.balloons()
                
                # Auto-redirect to results after 2 seconds
                time.sleep(2)
                st.switch_page("pages/4_📈_Results.py")
                
            else:
                st.error("❌ Payment failed. Please try again.")
                st.info("""
                **Troubleshooting Tips:**
                - Ensure your phone number is correct
                - Check your M-Pesa balance
                - Ensure you have mobile data
                - Try again in a few minutes
                """)
    
    # Demo mode notice
    st.markdown("---")
    st.info("""
    **💡 Demo Notice:** 
    This is a live M-Pesa integration. For demo purposes, payments are set to KES 1. 
    In production, you can adjust the amount as needed.
    """)

if __name__ == "__main__":
    main()