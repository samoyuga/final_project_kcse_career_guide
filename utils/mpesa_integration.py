import requests
import base64
import json
from datetime import datetime
import streamlit as st
from decouple import config
import hashlib
import time

class MpesaDarajaAPI:
    def __init__(self):
        # Load configuration from environment variables
        self.consumer_key = config('MPESA_CONSUMER_KEY', default='')
        self.consumer_secret = config('MPESA_CONSUMER_SECRET', default='')
        self.business_shortcode = config('MPESA_BUSINESS_SHORTCODE', default='174379')
        self.passkey = config('MPESA_PASSKEY', default='')
        self.callback_url = config('MPESA_CALLBACK_URL', default='https://your-domain.com/api/mpesa-callback')
        
        # Sandbox credentials for testing (fallback)
        self.sandbox_consumer_key = "your_sandbox_consumer_key"
        self.sandbox_consumer_secret = "your_sandbox_consumer_secret"
        self.sandbox_shortcode = "174379"
        self.sandbox_passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
        
        self.base_url = "https://sandbox.safaricom.co.ke"  # Change to production when ready
        self.access_token = None
        self.token_expiry = None
        
    def get_access_token(self):
        """Get M-Pesa API access token"""
        try:
            # Check if token is still valid
            if self.access_token and self.token_expiry and datetime.now() < self.token_expiry:
                return self.access_token
                
            # Use sandbox credentials if production credentials are not set
            if not self.consumer_key or not self.consumer_secret:
                consumer_key = self.sandbox_consumer_key
                consumer_secret = self.sandbox_consumer_secret
                st.warning("⚠️ Using Sandbox Mode - Configure production credentials for live payments")
            else:
                consumer_key = self.consumer_key
                consumer_secret = self.consumer_secret
            
            url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
            
            # Create authentication string
            auth_string = f"{consumer_key}:{consumer_secret}"
            encoded_auth = base64.b64encode(auth_string.encode()).decode()
            
            headers = {
                "Authorization": f"Basic {encoded_auth}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access_token')
                # Token expires in 1 hour (3599 seconds)
                self.token_expiry = datetime.now().timestamp() + 3599
                return self.access_token
            else:
                st.error(f"❌ Failed to get access token: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            st.error(f"❌ Error getting access token: {str(e)}")
            return None
    
    def generate_password(self, timestamp):
        """Generate M-Pesa API password"""
        try:
            shortcode = self.business_shortcode if self.business_shortcode else self.sandbox_shortcode
            passkey = self.passkey if self.passkey else self.sandbox_passkey
            
            data = f"{shortcode}{passkey}{timestamp}"
            return base64.b64encode(data.encode()).decode()
        except Exception as e:
            st.error(f"❌ Error generating password: {str(e)}")
            return None
    
    def format_phone_number(self, phone_number):
        """Format phone number to M-Pesa format (2547XXXXXXXX)"""
        try:
            # Remove any spaces, dashes, or other characters
            phone_number = ''.join(filter(str.isdigit, phone_number))
            
            # Handle different formats
            if phone_number.startswith('0'):
                return '254' + phone_number[1:]
            elif phone_number.startswith('+254'):
                return phone_number[1:]
            elif phone_number.startswith('254'):
                return phone_number
            else:
                # Assume it's already in correct format
                return phone_number
        except Exception as e:
            st.error(f"❌ Error formatting phone number: {str(e)}")
            return phone_number
    
    def initiate_stk_push(self, phone_number, amount, account_reference, transaction_desc="Career Guidance Service"):
        """Initiate M-Pesa STK push payment"""
        try:
            # Get access token
            access_token = self.get_access_token()
            if not access_token:
                return {
                    "success": False,
                    "error_code": "AUTH_FAILED",
                    "error_message": "Failed to authenticate with M-Pesa API"
                }
            
            # Format phone number
            formatted_phone = self.format_phone_number(phone_number)
            if not formatted_phone or len(formatted_phone) != 12:
                return {
                    "success": False,
                    "error_code": "INVALID_PHONE",
                    "error_message": "Invalid phone number format"
                }
            
            # Generate timestamp and password
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            password = self.generate_password(timestamp)
            if not password:
                return {
                    "success": False,
                    "error_code": "PASSWORD_ERROR",
                    "error_message": "Failed to generate transaction password"
                }
            
            # Determine shortcode to use
            shortcode = self.business_shortcode if self.business_shortcode else self.sandbox_shortcode
            
            # Prepare STK push request
            url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
            
            payload = {
                "BusinessShortCode": shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": int(amount),
                "PartyA": formatted_phone,
                "PartyB": shortcode,
                "PhoneNumber": formatted_phone,
                "CallBackURL": self.callback_url,
                "AccountReference": account_reference[:12],  # Max 12 characters
                "TransactionDesc": transaction_desc[:13]    # Max 13 characters
            }
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            st.info("🔄 Initiating M-Pesa payment...")
            with st.spinner("Sending payment request to M-Pesa..."):
                response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('ResponseCode') == '0':
                    return {
                        "success": True,
                        "response_code": data.get('ResponseCode'),
                        "customer_message": data.get('CustomerMessage'),
                        "checkout_request_id": data.get('CheckoutRequestID'),
                        "merchant_request_id": data.get('MerchantRequestID'),
                        "response_description": data.get('ResponseDescription')
                    }
                else:
                    return {
                        "success": False,
                        "error_code": data.get('ResponseCode', 'UNKNOWN_ERROR'),
                        "error_message": data.get('ResponseDescription', 'Unknown error occurred'),
                        "customer_message": data.get('CustomerMessage', '')
                    }
            else:
                error_msg = f"HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg = error_data.get('errorMessage', error_msg)
                except:
                    error_msg = response.text
                
                return {
                    "success": False,
                    "error_code": f"HTTP_{response.status_code}",
                    "error_message": error_msg
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error_code": "TIMEOUT",
                "error_message": "Request timed out. Please try again."
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error_code": "CONNECTION_ERROR",
                "error_message": "Network connection error. Please check your internet."
            }
        except Exception as e:
            return {
                "success": False,
                "error_code": "EXCEPTION",
                "error_message": f"Unexpected error: {str(e)}"
            }
    
    def check_transaction_status(self, checkout_request_id):
        """Check status of a transaction"""
        try:
            access_token = self.get_access_token()
            if not access_token:
                return None
            
            url = f"{self.base_url}/mpesa/stkpushquery/v1/query"
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            password = self.generate_password(timestamp)
            shortcode = self.business_shortcode if self.business_shortcode else self.sandbox_shortcode
            
            payload = {
                "BusinessShortCode": shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "CheckoutRequestID": checkout_request_id
            }
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            st.error(f"Error checking transaction status: {str(e)}")
            return None

def process_mpesa_payment(phone_number, amount, user_id):
    """Simple demo mode that always succeeds - replace with real M-Pesa integration in production"""
    
    # Display payment information
    st.info("💳 **M-Pesa Payment Initiation**")
    st.write(f"**Phone Number:** {phone_number}")
    st.write(f"**Amount:** KES {amount}")
    st.write(f"**Reference:** CAREER_{user_id}")
    st.write("---")
    
    # Demo mode notice
    st.warning("🔧 **DEMO MODE ACTIVE**")
    st.info("""
    **For testing purposes only:**
    - No actual M-Pesa transaction will occur
    - Career report will be generated immediately
    - Replace with real M-Pesa integration in production
    """)
    
    # Simulate payment processing
    with st.spinner("Processing demo payment..."):
        time.sleep(2)
    
    st.success("✅ **Demo Payment Successful!**")
    st.write("**Status:** Payment simulation completed")
    st.write("**Note:** In production, this would trigger real M-Pesa STK Push")
    
    # Simulate report generation delay
    with st.spinner("🎯 Generating your career report..."):
        time.sleep(2)
    
    st.balloons()
    st.success("🎉 **Career Report Generated Successfully!**")
    
    return True
def handle_mpesa_callback(callback_data):
    """Handle M-Pesa callback (for webhook endpoint)"""
    try:
        # This function would be called by your webhook endpoint
        st.write("Received M-Pesa callback:", callback_data)
        
        # Extract relevant data from callback
        result_code = callback_data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
        result_desc = callback_data.get('Body', {}).get('stkCallback', {}).get('ResultDesc')
        checkout_request_id = callback_data.get('Body', {}).get('stkCallback', {}).get('CheckoutRequestID')
        merchant_request_id = callback_data.get('Body', {}).get('stkCallback', {}).get('MerchantRequestID')
        
        # Process the result
        if result_code == 0:
            # Payment successful
            st.success(f"Payment completed successfully: {checkout_request_id}")
            # Update your database here
            return True
        else:
            # Payment failed
            st.error(f"Payment failed: {result_desc}")
            return False
            
    except Exception as e:
        st.error(f"Error processing callback: {str(e)}")
        return False