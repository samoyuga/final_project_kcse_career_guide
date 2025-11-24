# 🎓 KCSE Career Guidance Tool with M-Pesa Integration

An AI-powered career guidance system with real M-Pesa payments using Safaricom Daraja API.

## 🚀 Features

- 📚 KCSE Subject Analysis with validation
- 🎯 Skills & Interests Assessment
- 🤖 AI-Powered Career Recommendations
- 💳 Real M-Pesa Payments via Daraja API
- 📊 Detailed Career Reports with University Recommendations

## ⚙️ M-Pesa Daraja API Setup

### 1. Get API Credentials

1. **Create Daraja Account:**
   - Go to [Safaricom Daraja](https://developer.safaricom.co.ke/)
   - Register for a developer account
   - Create a new application

2. **Get Credentials:**
   - Consumer Key
   - Consumer Secret
   - Passkey (for STK Push)
   - Business Shortcode (PayBill or Till Number)

### 2. Environment Configuration

Create a `.env` file:

```env
# M-Pesa Daraja API Credentials
MPESA_CONSUMER_KEY=your_actual_consumer_key
MPESA_CONSUMER_SECRET=your_actual_consumer_secret
MPESA_BUSINESS_SHORTCODE=174379
MPESA_PASSKEY=your_actual_passkey
MPESA_CALLBACK_URL=https://your-app-url.herokuapp.com/api/mpesa-callback

# App Configuration
APP_ENV=production

3. Webhook Setup
For production, set up a webhook endpoint to receive M-Pesa callbacks:

python
# Example Flask endpoint for callbacks
@app.route('/api/mpesa-callback', methods=['POST'])
def mpesa_callback():
    data = request.get_json()
    # Process the callback data
    return jsonify({"ResultCode": 0, "ResultDesc": "Success"})
🛠️ Installation
Clone and Install:

bash
git clone https://github.com/yourusername/kcse-career-guide.git
cd kcse-career-guide
pip install -r requirements.txt
Configure Environment:

bash
cp .env.example .env
# Edit .env with your actual M-Pesa credentials
Run Locally:

bash
streamlit run app.py
🌐 Deployment
Streamlit Cloud Deployment
Push code to GitHub

Go to Streamlit Cloud

Connect your repository

Add environment variables in settings:

MPESA_CONSUMER_KEY

MPESA_CONSUMER_SECRET

MPESA_BUSINESS_SHORTCODE

MPESA_PASSKEY

MPESA_CALLBACK_URL

## Key Changes Made:

1. **Real Daraja API Integration**: Complete implementation of M-Pesa STK Push
2. **Proper Error Handling**: Comprehensive error messages and user feedback
3. **Phone Number Formatting**: Automatic formatting to M-Pesa standards
4. **Payment Status Tracking**: Database integration for payment records
5. **Webhook Ready**: Callback handling structure for production
6. **Environment Configuration**: Secure credential management
7. **Sandbox/Production Support**: Fallback to sandbox for testing

## Next Steps for Production:

1. **Get Daraja API credentials** from Safaricom
2. **Set up webhook endpoint** for payment callbacks
3. **Configure environment variables** in deployment platform
4. **Test thoroughly** with sandbox before going live
5. **Implement proper logging** and monitoring