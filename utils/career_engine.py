import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import os

class CareerEngine:
    def __init__(self):
        self.career_paths = self.load_career_paths()
        self.grade_points = {
            'A': 12, 'A-': 11, 'B+': 10, 'B': 9, 'B-': 8,
            'C+': 7, 'C': 6, 'C-': 5, 'D+': 4, 'D': 3, 'D-': 2, 'E': 1
        }
        
    def load_career_paths(self):
        """Load comprehensive career paths data for Kenyan system"""
        career_data = {
            "Medicine & Health Sciences": [
                {
                    "career": "Medical Doctor",
                    "required_subjects": ["Biology", "Chemistry", "Physics"],
                    "required_grades": {"Biology": "B+", "Chemistry": "B+", "Physics": "B", "Mathematics": "B+"},
                    "skills": ["Problem Solving", "Critical Thinking", "Communication", "Empathy", "Attention to Detail"],
                    "interests": ["Sciences", "Medicine", "Research", "Helping People", "Healthcare"],
                    "description": "Diagnose and treat illnesses, provide medical care to patients in hospitals and clinics",
                    "universities": ["University of Nairobi", "Kenyatta University", "Moi University", "JKUAT", "Mount Kenya University"],
                    "courses": ["Bachelor of Medicine and Surgery", "Bachelor of Dental Surgery"],
                    "cluster": "Medicine & Health Sciences"
                },
                {
                    "career": "Clinical Officer",
                    "required_subjects": ["Biology", "Chemistry"],
                    "required_grades": {"Biology": "C+", "Chemistry": "C+", "Mathematics": "C+"},
                    "skills": ["Communication", "Teamwork", "Problem Solving", "Empathy"],
                    "interests": ["Medicine", "Healthcare", "Community Service", "Helping People"],
                    "description": "Provide clinical care and medical services under supervision in various healthcare settings",
                    "universities": ["Kenya Medical Training College", "University of Nairobi", "Kenyatta University"],
                    "courses": ["Diploma in Clinical Medicine", "Bachelor of Clinical Medicine"],
                    "cluster": "Medicine & Health Sciences"
                },
                {
                    "career": "Pharmacist",
                    "required_subjects": ["Biology", "Chemistry", "Physics"],
                    "required_grades": {"Biology": "B", "Chemistry": "B+", "Mathematics": "B"},
                    "skills": ["Attention to Detail", "Analytical Thinking", "Communication", "Organization"],
                    "interests": ["Sciences", "Medicine", "Chemistry", "Healthcare"],
                    "description": "Prepare and dispense medications, provide drug information to healthcare professionals and patients",
                    "universities": ["University of Nairobi", "Kenyatta University", "Moi University", "Mount Kenya University"],
                    "courses": ["Bachelor of Pharmacy", "Doctor of Pharmacy"],
                    "cluster": "Medicine & Health Sciences"
                }
            ],
            "Engineering & Technology": [
                {
                    "career": "Software Engineer",
                    "required_subjects": ["Mathematics", "Physics"],
                    "required_grades": {"Mathematics": "B+", "Physics": "B", "English": "C+"},
                    "skills": ["Problem Solving", "Technical Skills", "Creativity", "Analytical Thinking", "Logic"],
                    "interests": ["Technology", "Computers", "Innovation", "Problem Solving", "Programming"],
                    "description": "Design, develop, and maintain software systems and applications for various platforms",
                    "universities": ["JKUAT", "University of Nairobi", "Strathmore University", "Kenyatta University", "Technical University of Kenya"],
                    "courses": ["Bachelor of Computer Science", "Bachelor of Software Engineering", "Bachelor of Information Technology"],
                    "cluster": "Engineering & Technology"
                },
                {
                    "career": "Civil Engineer",
                    "required_subjects": ["Mathematics", "Physics", "Chemistry"],
                    "required_grades": {"Mathematics": "B+", "Physics": "B", "Chemistry": "C+"},
                    "skills": ["Problem Solving", "Analytical Thinking", "Project Management", "Design"],
                    "interests": ["Engineering", "Construction", "Infrastructure", "Design", "Mathematics"],
                    "description": "Design and oversee construction of infrastructure projects like roads, buildings, and bridges",
                    "universities": ["University of Nairobi", "JKUAT", "Technical University of Kenya", "Moi University"],
                    "courses": ["Bachelor of Civil Engineering", "Bachelor of Construction Management"],
                    "cluster": "Engineering & Technology"
                },
                {
                    "career": "Electrical Engineer",
                    "required_subjects": ["Mathematics", "Physics", "Chemistry"],
                    "required_grades": {"Mathematics": "B+", "Physics": "B+", "Chemistry": "C+"},
                    "skills": ["Analytical Thinking", "Problem Solving", "Technical Skills", "Mathematics"],
                    "interests": ["Technology", "Engineering", "Electronics", "Innovation"],
                    "description": "Design, develop, and maintain electrical systems and electronic devices",
                    "universities": ["University of Nairobi", "JKUAT", "Moi University", "Technical University of Kenya"],
                    "courses": ["Bachelor of Electrical Engineering", "Bachelor of Electronic Engineering"],
                    "cluster": "Engineering & Technology"
                }
            ],
            "Business & Commerce": [
                {
                    "career": "Chartered Accountant",
                    "required_subjects": ["Mathematics", "Business Studies"],
                    "required_grades": {"Mathematics": "B", "English": "C+", "Business Studies": "C+"},
                    "skills": ["Analytical Thinking", "Organization", "Attention to Detail", "Communication", "Mathematics"],
                    "interests": ["Business", "Finance", "Numbers", "Analysis", "Accounting"],
                    "description": "Manage financial records, provide financial advice, ensure compliance with accounting standards",
                    "universities": ["Kenyatta University", "University of Nairobi", "Strathmore University", "Mount Kenya University", "USIU Africa"],
                    "courses": ["Bachelor of Commerce", "Bachelor of Business Administration", "Bachelor of Economics"],
                    "cluster": "Business & Commerce"
                },
                {
                    "career": "Business Manager",
                    "required_subjects": ["Mathematics", "Business Studies"],
                    "required_grades": {"Mathematics": "C+", "English": "C+", "Business Studies": "C+"},
                    "skills": ["Leadership", "Communication", "Strategic Thinking", "Decision Making"],
                    "interests": ["Business", "Management", "Entrepreneurship", "Leadership"],
                    "description": "Oversee business operations, manage teams, and make strategic decisions for organizational growth",
                    "universities": ["Kenyatta University", "University of Nairobi", "Strathmore University", "Mount Kenya University"],
                    "courses": ["Bachelor of Business Management", "Bachelor of Commerce", "Bachelor of Business Administration"],
                    "cluster": "Business & Commerce"
                }
            ],
            "Education & Social Sciences": [
                {
                    "career": "Secondary School Teacher",
                    "required_subjects": [],
                    "required_grades": {"English": "C+", "Mathematics": "C+"},
                    "skills": ["Communication", "Public Speaking", "Patience", "Leadership", "Teaching"],
                    "interests": ["Education", "Teaching", "Mentoring", "Community Development", "Subject Expertise"],
                    "description": "Educate students in specific subject areas at secondary level, develop lesson plans and assess student progress",
                    "universities": ["Kenyatta University", "University of Nairobi", "Moi University", "Egerton University", "Maseno University"],
                    "courses": ["Bachelor of Education", "Postgraduate Diploma in Education"],
                    "cluster": "Education & Social Sciences"
                },
                {
                    "career": "Social Worker",
                    "required_subjects": [],
                    "required_grades": {"English": "C+", "Kiswahili": "C+"},
                    "skills": ["Empathy", "Communication", "Problem Solving", "Counseling", "Community Service"],
                    "interests": ["Community Service", "Helping People", "Social Justice", "Psychology"],
                    "description": "Help individuals and communities overcome challenges and improve their quality of life",
                    "universities": ["University of Nairobi", "Kenyatta University", "Moi University", "Daystar University"],
                    "courses": ["Bachelor of Social Work", "Bachelor of Arts in Sociology"],
                    "cluster": "Education & Social Sciences"
                }
            ],
            "Agriculture & Environmental Sciences": [
                {
                    "career": "Agricultural Engineer",
                    "required_subjects": ["Mathematics", "Physics", "Biology"],
                    "required_grades": {"Mathematics": "B", "Physics": "C+", "Biology": "C+"},
                    "skills": ["Problem Solving", "Technical Skills", "Analytical Thinking", "Innovation"],
                    "interests": ["Agriculture", "Technology", "Environment", "Engineering"],
                    "description": "Design agricultural machinery and equipment, develop sustainable farming practices",
                    "universities": ["JKUAT", "University of Nairobi", "Egerton University", "Moi University"],
                    "courses": ["Bachelor of Agricultural Engineering", "Bachelor of Science in Agricultural Engineering"],
                    "cluster": "Agriculture & Environmental Sciences"
                },
                {
                    "career": "Environmental Scientist",
                    "required_subjects": ["Biology", "Chemistry", "Geography"],
                    "required_grades": {"Biology": "C+", "Chemistry": "C+", "Mathematics": "C+"},
                    "skills": ["Research", "Analytical Thinking", "Problem Solving", "Data Analysis"],
                    "interests": ["Environment", "Sciences", "Research", "Conservation"],
                    "description": "Study environmental problems and develop solutions to protect natural resources",
                    "universities": ["Kenyatta University", "University of Nairobi", "Egerton University", "Moi University"],
                    "courses": ["Bachelor of Environmental Science", "Bachelor of Science in Environmental Studies"],
                    "cluster": "Agriculture & Environmental Sciences"
                }
            ]
        }
        return career_data
    
    def grade_to_points(self, grade):
        """Convert grade to numerical points"""
        return self.grade_points.get(grade, 0)
    
    def calculate_subject_score(self, user_grades, career_requirements):
        """Calculate how well user subjects match career requirements"""
        score = 0
        total_possible = 0
        
        for subject, required_grade in career_requirements.items():
            user_grade = user_grades.get(subject, "Not Taken")
            if user_grade != "Not Taken" and user_grade != "Select Grade":
                user_points = self.grade_to_points(user_grade)
                required_points = self.grade_to_points(required_grade)
                
                if user_points >= required_points:
                    score += 100
                else:
                    # Partial credit based on how close they are
                    score += (user_points / required_points) * 100
                total_possible += 100
        
        return (score / total_possible * 100) if total_possible > 0 else 0
    
    def calculate_skills_match(self, user_skills, career_skills):
        """Calculate skills similarity"""
        if not career_skills:
            return 0
            
        user_skills_set = set(user_skills)
        career_skills_set = set(career_skills)
        
        if len(career_skills_set) == 0:
            return 0
            
        intersection = user_skills_set.intersection(career_skills_set)
        return (len(intersection) / len(career_skills_set)) * 100
    
    def calculate_interests_match(self, user_interests, career_interests):
        """Calculate interests similarity"""
        if not career_interests:
            return 0
            
        user_interests_set = set(user_interests)
        career_interests_set = set(career_interests)
        
        if len(career_interests_set) == 0:
            return 0
            
        intersection = user_interests_set.intersection(career_interests_set)
        return (len(intersection) / len(career_interests_set)) * 100
    
    def generate_recommendations(self, subjects_grades, skills_interests):
        """Generate career recommendations based on user profile"""
        recommendations = []
        
        # Filter out "Not Taken" and "Select Grade" subjects
        user_subjects = {subject: grade for subject, grade in subjects_grades.items() 
                        if grade not in ["Not Taken", "Select Grade"]}
        user_skills = skills_interests['skills']
        user_interests = skills_interests['interests']
        
        for cluster, careers in self.career_paths.items():
            for career in careers:
                # Calculate subject match
                subject_match = self.calculate_subject_score(user_subjects, career.get('required_grades', {}))
                
                # Skip careers where subject requirements are not met (below 50%)
                if subject_match < 50:
                    continue
                
                # Calculate skills match
                skills_match = self.calculate_skills_match(user_skills, career.get('skills', []))
                
                # Calculate interests match
                interests_match = self.calculate_interests_match(user_interests, career.get('interests', []))
                
                # Overall score (weighted average)
                overall_score = (subject_match * 0.5 + skills_match * 0.3 + interests_match * 0.2)
                
                # Generate reasoning
                reasoning = self.generate_reasoning(user_subjects, user_skills, user_interests, career, subject_match, skills_match, interests_match)
                
                recommendations.append({
                    'career': career['career'],
                    'cluster': cluster,
                    'match_score': round(overall_score, 1),
                    'subject_match': round(subject_match, 1),
                    'skills_match': round(skills_match, 1),
                    'interests_match': round(interests_match, 1),
                    'description': career['description'],
                    'recommended_courses': career['courses'],
                    'universities': career['universities'],
                    'reasoning': reasoning,
                    'required_subjects': career.get('required_subjects', []),
                    'required_grades': career.get('required_grades', {})
                })
        
        # Sort by overall score and return top recommendations
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        
        return {
            'top_careers': recommendations[:5],
            'all_careers': recommendations,
            'user_profile': {
                'subjects_count': len(user_subjects),
                'skills_count': len(user_skills),
                'interests_count': len(user_interests)
            }
        }
    
    def generate_reasoning(self, user_subjects, user_skills, user_interests, career, subject_match, skills_match, interests_match):
        """Generate reasoning for career recommendation"""
        reasoning_parts = []
        
        # Subject reasoning
        strong_subjects = []
        missing_subjects = []
        
        for subject, required_grade in career.get('required_grades', {}).items():
            user_grade = user_subjects.get(subject, "Not Taken")
            if user_grade != "Not Taken" and user_grade != "Select Grade":
                user_points = self.grade_to_points(user_grade)
                required_points = self.grade_to_points(required_grade)
                if user_points >= required_points:
                    strong_subjects.append(f"strong {user_grade} in {subject}")
                else:
                    missing_subjects.append(f"higher grade in {subject} (needs {required_grade})")
        
        if strong_subjects:
            reasoning_parts.append(f"Your {' and '.join(strong_subjects)} meet the academic requirements.")
        
        if missing_subjects:
            reasoning_parts.append(f"Consider improving: {', '.join(missing_subjects)}")
        
        # Skills reasoning
        matching_skills = set(user_skills).intersection(set(career.get('skills', [])))
        if matching_skills:
            reasoning_parts.append(f"Your skills in {', '.join(matching_skills)} align well with this career.")
        
        # Interests reasoning
        matching_interests = set(user_interests).intersection(set(career.get('interests', [])))
        if matching_interests:
            reasoning_parts.append(f"Your interests in {', '.join(matching_interests)} match this field perfectly.")
        
        return " ".join(reasoning_parts) if reasoning_parts else "This career aligns with your overall academic profile and personal attributes."
    
    def get_career_insights(self, recommendations):
        """Generate insights about the career recommendations"""
        insights = []
        
        if not recommendations['top_careers']:
            insights.append("Consider improving your grades in core subjects or exploring different skill combinations.")
            return insights
        
        top_career = recommendations['top_careers'][0]
        
        if top_career['match_score'] >= 80:
            insights.append("🎯 Excellent match! You have strong alignment with your top career recommendation.")
        elif top_career['match_score'] >= 60:
            insights.append("✅ Good match! Your profile aligns well with several career paths.")
        else:
            insights.append("💡 Consider exploring related fields or improving specific subject areas.")
        
        # Subject-based insights
        if top_career['subject_match'] < top_career['match_score']:
            insights.append("📚 Focus on maintaining strong academic performance in required subjects.")
        
        # Skills-based insights
        if top_career['skills_match'] > top_career['subject_match']:
            insights.append("🛠️ Your skills are a strong asset - consider how to further develop them.")
        
        return insights