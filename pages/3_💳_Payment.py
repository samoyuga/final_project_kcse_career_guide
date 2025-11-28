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
        st.write(f"**Amount:** KES 20")
        
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
        
        **💡 Important:** Use the same phone number registered above
        """)
    
    # Payment section
    st.markdown("---")
    st.header("🔐 Secure M-Pesa Payment")
    
    payment_col1, payment_col2 = st.columns([1, 1])
    
    with payment_col1:
        st.subheader("Payment Details")
        st.info(f"""
        **Lipa na M-Pesa Details:**
        - Amount: KES 20
        - Till Number: **6910505**
        - Account: CAREER_{user_id}
        - No extra charges
        
        **Manual Payment Option:**
        - Go to M-Pesa Menu
        - Lipa na M-Pesa
        - Buy Goods and Services
        - Enter Till: **6910505**
        - Amount: **20**
        - Enter your PIN
        """)
    
    with payment_col2:
        st.subheader("Initiate Payment")
        
        # Payment confirmation
        st.warning("**Payment Amount: KES 20**")
        
        if st.button("💰 Pay KES 20 via M-Pesa", type="primary", use_container_width=True):
            with st.spinner("Initiating M-Pesa payment..."):
                try:
                    # Process M-Pesa payment without till_number parameter
                    payment_success = process_mpesa_payment(
                        student_info['phone'], 
                        20,  # Amount
                        user_id
                    )
                except TypeError as e:
                    st.error(f"❌ Payment configuration error: {e}")
                    st.info("Please check your M-Pesa integration setup")
                    payment_success = False
            
            if payment_success:
                # Save payment record
                save_payment(user_id, 20, f"CAREER_{user_id}", "completed")
                
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
                
                # Show success message before redirect
                st.info("📊 Redirecting to your career report...")
                
                # Auto-redirect to results after 3 seconds
                time.sleep(3)
                st.switch_page("pages/4_📈_Results.py")
                
            else:
                st.error("❌ Payment failed. Please try again.")
                st.info("""
                **Troubleshooting Tips:**
                - Ensure your phone number is correct and has M-Pesa
                - Check your M-Pesa balance (KES 20 required)
                - Ensure you have mobile data connectivity
                - Try the manual Lipa na M-Pesa option
                - Contact support if issues persist
                """)
    
    # Manual payment confirmation section
    st.markdown("---")
    st.subheader("🔧 Manual Payment Confirmation")
    
    with st.expander("If you paid manually or having issues"):
        st.markdown("""
        If you've already made payment via Lipa na M-Pesa but the system didn't detect it automatically,
        or if you're experiencing technical issues:
        """)
        
        confirm_col1, confirm_col2 = st.columns(2)
        
        with confirm_col1:
            transaction_code = st.text_input("Enter M-Pesa Transaction Code", placeholder="e.g., QAZ45WER90")
            
        with confirm_col2:
            if st.button("✅ Confirm Manual Payment", use_container_width=True):
                if transaction_code:
                    # Verify manual payment
                    manual_payment_success = verify_manual_payment(transaction_code, user_id)
                    
                    if manual_payment_success:
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
                        
                        st.success("✅ Payment verified! Your report is ready.")
                        st.balloons()
                        time.sleep(2)
                        st.switch_page("pages/4_📈_Results.py")
                    else:
                        st.error("❌ Could not verify payment. Please check transaction code or contact support.")
                else:
                    st.warning("⚠️ Please enter your M-Pesa transaction code")
    
    # Support information
    st.markdown("---")
    st.info("""
    **📞 Need Help?**
    - Payment Issues: 0723349693
    - Technical Support: 0723349693
    - Email: your-email@example.com
    
    **💼 Business Info:** 
    This is a live Lipa na M-Pesa Buy Goods till number. All payments go directly to registered business account.
    """)

def verify_manual_payment(transaction_code, user_id):
    """
    Verify manual payment - you'll need to implement this based on your M-Pesa API
    For now, this is a placeholder that returns True for demo purposes
    """
    # TODO: Implement actual M-Pesa transaction verification
    # This could involve checking your M-Pesa records or using M-Pesa API
    if transaction_code and len(transaction_code) > 5:
        save_payment(user_id, 20, f"CAREER_{user_id}", "completed", transaction_code)
        return True
    return False

if __name__ == "__main__":
    main()