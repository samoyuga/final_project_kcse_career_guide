KCSE Career Guide 🎓
A comprehensive AI-powered career guidance system for Kenyan KCSE students that provides personalized career recommendations based on subjects, skills, and interests with integrated M-Pesa payments.



🌟 Live Application
🌐 Live Demo: https://kcsecareerguide.streamlit.app/

📋 Overview
The KCSE Career Guide is an intelligent platform that helps Kenyan high school students make informed career decisions after their KCSE examinations. The system analyzes students' academic performance, skills, and interests to provide personalized career recommendations aligned with KUCCPS cluster requirements.

🚀 Key Features
📚 Comprehensive Subject Analysis
Complete KCSE subject coverage (All 7-9 subjects)

Official KUCCPS cluster grouping compliance

Real-time subject requirement validation

Grade-based career pathway matching

🎯 Intelligent Career Matching
60% Weight on Interests & Skills - Prioritizes student passions

40% Weight on Academic Performance - Considers subject requirements

Enhanced medical career specialization

20+ KUCCPS career clusters with 500+ degree programmes

💳 Integrated Payment System
Live M-Pesa integration (Lipa na M-Pesa)

Till Number: 6910505

Secure payment processing

Instant report generation after payment

📊 Personalized Reports
Top 15 career recommendations

Detailed match scoring breakdown

University and course information

Career pathway insights

🏗️ System Architecture
text
KCSE Career Guide
├── Frontend (Streamlit)
│   ├── Home Page - Welcome & Introduction
│   ├── Career Analysis - Subject & Skills Input
│   ├── Payment - M-Pesa Integration
│   └── Results - Personalized Career Report
├── Backend Logic
│   ├── Career Engine - Recommendation Algorithm
│   ├── Database - User Data Management
│   └── M-Pesa API - Payment Processing
└── Data
    ├── KUCCPS Clusters (20 Clusters)
    ├── Degree Programmes (500+ Courses)
    └── Subject Requirements
🎓 Supported Career Clusters
Law & Legal Studies

Business, Hospitality & Tourism

Social Sciences, Media & Arts

Geosciences & Geography

Engineering & Technology

Architecture & Construction

Computing & IT

Agribusiness & Management

General Sciences

Mathematics, Economics & Statistics

Design & Fashion

Sports Science

🏥 Medicine & Health Sciences (Enhanced Matching)

History & Archaeology

Agriculture & Environment

Geography & Planning

Languages & Linguistics

Music & Performing Arts

Education & Teaching

Religious Studies & Theology

💰 Pricing
Service Fee: KES 20 per career report

Payment Method: Lipa na M-Pesa (Till: 6910505)

Service: AI-powered personalized career guidance report

🔧 Installation & Local Development
Prerequisites
Python 3.8+

pip package manager

Git

Step-by-Step Setup
Clone the Repository

bash
git clone https://github.com/samoyuga/final_project_kcse_career_guide.git
cd kcse-career-guide
Create Virtual Environment

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies

bash
pip install -r requirements.txt
Run the Application

bash
streamlit run app.py
Access the Application

Open your browser and go to: http://localhost:8501

Required Dependencies
txt
streamlit==1.28.0
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
plotly==5.15.0
mysql-connector-python==8.1.0
python-dotenv==1.0.0
requests==2.31.0
cryptography==41.0.4

🌐 Deployment
Streamlit Cloud Deployment
Push to GitHub

bash
git add .
git commit -m "Deploy KCSE Career Guide"
git push origin main
Deploy on Streamlit Cloud

Go to share.streamlit.io

Sign in with GitHub

Click "New app"

Select repository, branch, and main file

Click "Deploy"

Configure Secrets (Optional - for production M-Pesa)

Go to app settings → Secrets

Add your M-Pesa API credentials

Deployment URL
Your app will be available at:
https://your-username-kcse-career-guide-app.streamlit.app

📱 How to Use
Step 1: Complete Career Analysis
Navigate to "Career Analysis" page

Enter your KCSE subjects and grades

Select your skills and interests

Fill in personal details

Submit for validation

Step 2: Make Payment
Review your order summary

Click "Pay via M-Pesa" (KES 20)

Complete payment on your phone

Wait for automatic confirmation

Step 3: Get Your Report
View personalized career recommendations

See match scores and reasoning

Explore different career clusters

Download or share your results

🎯 Algorithm Features
Intelligent Weighting System
Interests: 30% weight

Skills: 30% weight

Subjects: 40% weight

Medical Career Bonus: +30% for medicine interests

Enhanced Matching
Direct interest-to-career mapping

Skills compatibility analysis

Subject requirement validation

Cluster-specific prioritization

🔒 Privacy & Security
No personal data stored permanently

Session-based data management

Secure M-Pesa transactions

No sharing of student information

📞 Support
Technical Support: 0723349693
Payment Issues: 0723349693
Email: your-email@example.com

Business Information
Business Name: KCSE Career Guide

M-Pesa Till: 6910505 (Lipa na M-Pesa)

Service: AI Career Guidance Reports

🐛 Troubleshooting
Common Issues
Payment Failed

Ensure sufficient M-Pesa balance

Use correct phone number

Check network connection

Form Validation Errors

Select at least 7 subjects

Include 2+ sciences and 1+ humanity

Complete all mandatory fields

Career Recommendations Not Showing

Ensure all subject grades are selected

Select at least one skill and interest

Meet minimum subject requirements

🔄 Future Enhancements
University-specific cut-off points

Scholarship opportunity matching

Career growth pathway visualization

Mobile app development

Multi-language support

Advanced analytics dashboard

🤝 Contributing
We welcome contributions! Please feel free to submit pull requests or open issues for:

Bug fixes

New features

Documentation improvements

Translation support

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
Kenya Universities and Colleges Central Placement Service (KUCCPS)

Safaricom M-Pesa API

Streamlit Community

Kenyan Ministry of Education