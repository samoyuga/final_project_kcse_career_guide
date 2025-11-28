import requests
import base64
from datetime import datetime
import streamlit as st
from decouple import config
import time

class MpesaDarajaAPI:
    def __init__(self):
        # Load LIVE configuration from environment variables
        self.consumer_key = config('MPESA_CONSUMER_KEY')
        self.consumer_secret = config('MPESA_CONSUMER_SECRET')
        self.business_shortcode = config('MPESA_BUSINESS_SHORTCODE')  # e.g., 6910505
        self.passkey = config('MPESA_PASSKEY')
        self.callback_url = config('MPESA_CALLBACK_URL')
        
        # LIVE base URL
        self.base_url = "https://api.safaricom.co.ke"
        self.access_token = None
        self.token_expiry = None

    def get_access_token(self):
        """Get M-Pesa API access token"""
        try:
            if self.access_token and self.token_expiry and datetime.now().timestamp() < self.token_expiry:
                return self.access_token

            auth_url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
            auth_string = f"{self.consumer_key}:{self.consumer_secret}"
            encoded_auth = base64.b64encode(auth_string.encode()).decode()
            headers = {"Authorization": f"Basic {encoded_auth}"}

            response = requests.get(auth_url, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access_token')
                self.token_expiry = datetime.now().timestamp() + 3599
                return self.access_token
            else:
                st.error(f"❌ Access token error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            st.error(f"❌ Access token exception: {str(e)}")
            return None

    def format_phone_number(self, phone_number):
        """Format phone number to 2547XXXXXXXX"""
        phone_number = ''.join(filter(str.isdigit, phone_number))
        if phone_number.startswith('0'):
            return '254' + phone_number[1:]
        elif phone_number.startswith('+254'):
            return phone_number[1:]
        elif phone_number.startswith('254'):
            return phone_number
        return phone_number

    def generate_password(self, timestamp):
        """Generate M-Pesa password for STK Push"""
        data = f"{self.business_shortcode}{self.passkey}{timestamp}"
        return base64.b64encode(data.encode()).decode()

    def initiate_stk_push(self, phone_number, amount, account_reference="Order", transaction_desc="Payment"):
        """Initiate LIVE STK Push for Buy Goods Till"""
        try:
            access_token = self.get_access_token()
            if not access_token:
                return {"success": False, "error_message": "Authentication failed"}

            formatted_phone = self.format_phone_number(phone_number)
            if len(formatted_phone) != 12:
                return {"success": False, "error_message": "Invalid phone number format"}

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            password = self.generate_password(timestamp)
            shortcode = self.business_shortcode

            payload = {
                "BusinessShortCode": shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerBuyGoodsOnline",
                "Amount": int(amount),
                "PartyA": formatted_phone,
                "PartyB": shortcode,
                "PhoneNumber": formatted_phone,
                "CallBackURL": self.callback_url,
                "AccountReference": account_reference[:12],
                "TransactionDesc": transaction_desc[:13]
            }

            headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
            response = requests.post(f"{self.base_url}/mpesa/stkpush/v1/processrequest",
                                     json=payload, headers=headers, timeout=30)

            if response.status_code == 200:
                data = response.json()
                if data.get('ResponseCode') == '0':
                    return {"success": True, **data}
                else:
                    return {"success": False, "error_message": data.get('ResponseDescription')}
            else:
                return {"success": False, "error_message": response.text}
        except Exception as e:
            return {"success": False, "error_message": str(e)}

    def check_transaction_status(self, checkout_request_id):
        """Query transaction status"""
        try:
            access_token = self.get_access_token()
            if not access_token:
                return None

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            password = self.generate_password(timestamp)

            payload = {
                "BusinessShortCode": self.business_shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "CheckoutRequestID": checkout_request_id
            }

            headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
            response = requests.post(f"{self.base_url}/mpesa/stkpushquery/v1/query",
                                     json=payload, headers=headers, timeout=30)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            st.error(f"Transaction status error: {str(e)}")
            return None

# Optional: Demo function for Streamlit until payment is received
def process_mpesa_payment(phone_number, amount, user_id):
    st.info("💳 **M-Pesa Payment Initiation (LIVE)**")
    st.write(f"Phone: {phone_number}, Amount: KES {amount}, Reference: CAREER_{user_id}")
    st.warning("⚠️ Ensure your callback URL is reachable for payment confirmation.")
    return True

def handle_mpesa_callback(callback_data):
    try:
        result = callback_data.get('Body', {}).get('stkCallback', {})
        if result.get('ResultCode') == 0:
            st.success(f"Payment successful: {result.get('CheckoutRequestID')}")
            return True
        else:
            st.error(f"Payment failed: {result.get('ResultDesc')}")
            return False
    except Exception as e:
        st.error(f"Callback error: {str(e)}")
        return False
