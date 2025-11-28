import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import re

class CareerEngine:
    def __init__(self):
        self.kuccps_clusters = self.load_kuccps_clusters()
        self.grade_points = {
            'A': 12, 'A-': 11, 'B+': 10, 'B': 9, 'B-': 8,
            'C+': 7, 'C': 6, 'C-': 5, 'D+': 4, 'D': 3, 'D-': 2, 'E': 1
        }
        self.subject_mapping = {
            'MAT ALTERNATIVE A': 'Mathematics', 'MAT ALTERNATIVE B': 'Mathematics',
            'MATHEMATICS ALTERNATIVE A': 'Mathematics', 'MATHEMATICS ALTERNATIVE B': 'Mathematics',
            'PHY': 'Physics', 'CHE': 'Chemistry', 'BIO': 'Biology', 
            'GEO': 'Geography', 'HAG': 'History', 'HISTORY': 'History',
            'CRE': 'CRE', 'IRE': 'IRE', 'HRE': 'HRE', 
            'ENG': 'English', 'KIS': 'Kiswahili',
            'FRE': 'French', 'GER': 'German', 'MUS': 'Music',
            'AGRIC': 'Agriculture', 'BST': 'Business Studies',
            'COMP': 'Computer Studies', 'HSC': 'Home Science',
            'ARD': 'Art & Design', 'SSE': 'Social Studies',
            'GSC': 'General Science'
        }
        
        # Enhanced interest mappings with stronger weights for medical fields
        self.enhanced_interest_mappings = {
            'Medicine': ['medicine', 'healthcare', 'biology', 'sciences', 'research', 'helping_people'],
            'Technology': ['technology', 'computers', 'programming', 'innovation', 'engineering'],
            'Engineering': ['engineering', 'technology', 'innovation', 'design', 'construction'],
            'Business': ['business', 'entrepreneurship', 'management', 'finance', 'commerce'],
            'Arts': ['arts', 'design', 'creativity', 'media', 'culture'],
            'Sciences': ['sciences', 'research', 'biology', 'chemistry', 'physics', 'medicine'],
            'Education': ['education', 'teaching', 'mentoring', 'community_development'],
            'Agriculture': ['agriculture', 'environment', 'farming', 'sustainability'],
            'Law': ['law', 'justice', 'politics', 'governance'],
            'Environment': ['environment', 'conservation', 'sustainability', 'nature'],
            'Politics': ['politics', 'governance', 'social_issues', 'law'],
            'Sports': ['sports', 'fitness', 'health', 'physical_activity'],
            'Music': ['music', 'performance', 'arts', 'creativity'],
            'Writing': ['writing', 'communication', 'media', 'journalism'],
            'Research': ['research', 'sciences', 'medicine', 'analysis'],
            'Community Service': ['community_service', 'helping_people', 'medicine', 'education'],
            'Entrepreneurship': ['entrepreneurship', 'business', 'innovation', 'management'],
            'Design': ['design', 'creativity', 'arts', 'innovation'],
            'Mathematics': ['mathematics', 'analysis', 'engineering', 'sciences']
        }
        
    def load_kuccps_clusters(self):
        """Load all KUCCPS clusters with complete programme data"""
        return {
            # CLUSTER 1 - LAW
            1: {
                'name': 'Law',
                'programmes': ['Bachelor of Laws (LL.B.)'],
                'subject_requirements': {
                    'Subject1': {'subjects': ['English'], 'min_grade': 'B'},
                    'Subject2': {'subjects': ['Mathematics', 'Biology', 'Physics', 'Chemistry'], 'min_grade': 'C+'},
                    'Subject3': {'subjects': ['History', 'Geography', 'CRE', 'IRE', 'HRE'], 'min_grade': 'C+'},
                    'Subject4': {'subjects': ['Business Studies', 'Computer Studies', 'Agriculture', 'Home Science', 'Art & Design', 'Music', 'French', 'German'], 'min_grade': 'C+'}
                },
                'skills': ['analytical', 'communication', 'research', 'critical_thinking', 'persuasion', 'logical_reasoning'],
                'interests': ['law', 'justice', 'politics', 'debate', 'social_issues', 'governance']
            },
            
            # CLUSTER 2 - BUSINESS & HOSPITALITY
            2: {
                'name': 'Business, Hospitality & Related',
                'programmes': [
                    'Bachelor in Business Administration', 'Bachelor in Business Administration, With IT',
                    'Bachelor of Business and Office Management', 'Bachelor of Business Management',
                    'Bachelor of Business Management (Marine Business Management)', 'Bachelor of Business Management (Aviation Management)',
                    'Bachelor of Art (Business Issues, With IT)', 'Bachelor of Science (Research Management and Information Technology)',
                    'Bachelor of Co-operative Management', 'Bachelor of Co-operative Business', 'Bachelor of Co-operative and Community Development',
                    'Bachelor of Secretarial Management and Administration', 'Bachelor of Technology (Office Administration and Technology)',
                    'Bachelor of Entrepreneurship & Small Business Management', 'Bachelor of Entrepreneurship and Small Business',
                    'Bachelor of Science (Entrepreneurship and Small Enterprise Management)', 'Bachelor of Science (Entrepreneurship Studies)',
                    'Bachelor of Science in Entrepreneurship', 'Bachelor of Procurement and Control Management',
                    'Bachelor of Procurement and Supply Chain Management', 'Bachelor of Purchasing & Supplies Management',
                    'Bachelor of Supply Chain Management', 'Bachelor of Logistics and Supply Chain Management',
                    'Bachelor of Procurement and Supplies Management', 'Bachelor of Purchasing and Supplies Management',
                    'Bachelor of Science (Management Sciences)', 'Bachelor of Science in Strategic Management',
                    'Bachelor of Science (Strategic Management)', 'Bachelor of Science in International Business Management',
                    'Bachelor of Science in Marketing With IT', 'Bachelor of Science in Co-operative and Entrepreneurship Management',
                    'Bachelor of Project Planning and Management', 'Bachelor of Science (Project Planning Management)',
                    'Bachelor of Science in Project Management', 'Bachelor of Human Resources Management',
                    'Bachelor of Science (Human Resource Management)', 'Bachelor of Human Resource Management',
                    'Bachelor of Science in Human Resource Management, With IT', 'Bachelor of Science (Hospitality & Tourism Management)',
                    'Bachelor of Science (Hospitality Management)', 'Bachelor of Sustainable Tourism & Hospitality Management',
                    'Bachelor of Tourism & Trade Management', 'Bachelor of Travel & Travel Operations Management',
                    'Bachelor of Science in Travel and Tourism Management', 'Bachelor of Catering & World Management',
                    'Bachelor of Retail and Hospitality Management', 'Bachelor of International Tourism Management',
                    'Bachelor of Science (Hospitality and Tourism Management)', 'Bachelor of Science (Fairman Management)',
                    'Bachelor of Science in Hospitality Management', 'Bachelor of Technology (Institutional Planning and Accommodation)',
                    'Bachelor of Technology in Hotel & Hospitality Management', 'Bachelor of Tourism Management',
                    'Bachelor of Travel and Travel Operations Management', 'Bachelor of Science (Food Operations Management)',
                    'Bachelor of Science in Food Services and Hospitality Management'
                ],
                'subject_requirements': {
                    'Subject1': {'subjects': ['Mathematics'], 'min_grade': 'C+'},
                    'Subject2': {'subjects': ['English', 'Kiswahili'], 'min_grade': 'C+'},
                    'Subject3': {'subjects': ['Biology', 'Physics', 'Chemistry'], 'min_grade': 'C+'},
                    'Subject4': {'subjects': ['History', 'Geography', 'CRE', 'IRE', 'HRE', 'Business Studies', 'Computer Studies', 'Agriculture', 'Home Science'], 'min_grade': 'C+'}
                },
                'skills': ['leadership', 'numeracy', 'communication', 'strategic_thinking', 'customer_service', 'organization'],
                'interests': ['business', 'entrepreneurship', 'management', 'finance', 'hospitality', 'tourism']
            },
            
            # CLUSTER 3 - SOCIAL SCIENCES, MEDIA, ARTS
            3: {
                'name': 'Social Sciences, Media Studies, Fine Arts, Film, Animation, Graphics & Related',
                'programmes': [
                    'Bachelor of Arts', 'Bachelor of Arts (With IT)', 'Bachelor of Applied Communication',
                    'Bachelor of Science (Communication and Public Relations)', 'Bachelor of Arts (Applied Linguistics)',
                    'Bachelor of Science (Communication & Journalism)', 'Bachelor of Arts (Communications & Media)',
                    'Bachelor of Science (Citizens & Public Relations)', 'Bachelor of Arts (Drama and Theatre Studies, With IT)',
                    'Bachelor of Communication & Public Relations', 'Bachelor of Communication and Public Relations',
                    'Bachelor of Science (Communication and Journalism)', 'Bachelor of Arts (International Relations and Diplomas, With IT)',
                    'Bachelor of Arts in Government and International Relations', 'Bachelor of Arts in International Relations',
                    'Bachelor of Arts Language and Communication, With IT', 'Bachelor of Arts (Linguistics, Media and Communication)',
                    'Bachelor of Arts (Literature, With IT)', 'Bachelor of Arts (Literature)', 'Bachelor of Arts in Linguistics and Literature',
                    'Bachelor of Arts (Theatre Arts & Film Technology)', 'Bachelor of Arts (Transactions and Interventions)',
                    'Bachelor of Communication & Journalism', 'Bachelor of Communication and Media Studies',
                    'Bachelor of Journalism & Mass Communication', 'Bachelor of Arts in Mass Communication',
                    'Bachelor of Science in Mass Communication', 'Bachelor of Mass Communication',
                    'Bachelor of Arts (English & Communication)', 'Bachelor of Arts (Straight and Communication)',
                    'Bachelor of Psychology (With IT)', 'Bachelor of Science (Counseling Psychology)', 'Bachelor of Arts (Foundering Psychology)',
                    'Bachelor of Arts (Psychology)', 'Bachelor of Arts in Counselling Psychology', 'Bachelor of Psychology',
                    'Bachelor of Arts (Sociology and Social Work)', 'Bachelor of Arts (Social Work)', 'Bachelor of Social Work',
                    'Bachelor of Social Work and Administration', 'Bachelor of Arts (Sociology and Anthropology, With IT)',
                    'Bachelor of Conflict Resolution and Humanitarian Assistance', 'Bachelor of Arts (Sociology)',
                    'Bachelor of Science in Sociology', 'Bachelor of Science in Public Administration and Leadership',
                    'Bachelor of Science (Disaster Mitigation and Sustainable Development)', 'Bachelor of Science in Medical Social Work',
                    'Bachelor of Science (Disaster Risk Management and Sustainable Development)', 'Bachelor of Arts (Disaster Management, With IT)',
                    'Bachelor of Disaster Management & International Diplomacy', 'Bachelor of Arts in Community Development',
                    'Bachelor of Science (Disaster Preparedness and Environment Technology)', 'Bachelor of Arts (Peace and Conflict Studies)',
                    'Bachelor of Arts Community Development', 'Bachelor of Community Development', 'Bachelor of Development Studies',
                    'Bachelor of Arts in Development Studies', 'Bachelor of Arts (Gender)', 'Bachelor of Science (Community Development)',
                    'Bachelor of Science (Public Management and Development)', 'Bachelor of Science in Community Development',
                    'Bachelor of Public Management and Development', 'Bachelor of Science (Community Development and Environment)',
                    'Bachelor of Science in Development Studies', 'Bachelor of Community Development and Environment',
                    'Bachelor of Arts (Developmental and Policy Studies)', 'Bachelor of Science (Community Resource Management)',
                    'Bachelor of Arts in Management', 'Bachelor of Arts in Leadership and Philosophy',
                    'Bachelor of Arts (Fine Art, With IT)', 'Bachelor of Science (Graphic, Communication and Advertising)',
                    'Bachelor of Arts (Fine Arts)', 'Bachelor of Science (Graphic, Comm. & Advertising)',
                    'Bachelor of Science in Gaming and Animation Technology', 'Bachelor of Arts (Design)',
                    'Bachelor of Arts (Interior Design, With IT)', 'Bachelor of Arts (Textiles, Apparel Design and Fashion Merchandising, With IT)',
                    'Bachelor of Science (Apparel & Fashion Technology)', 'Bachelor of Science (Clothing Textile & Interior Design)',
                    'Bachelor of Science (Fashion Design & Marketing)', 'Bachelor of Science (Fashion Design and Textile Technology)',
                    'Bachelor of Science in Fashion Design and Marketing'
                ],
                'subject_requirements': {
                    'Subject1': {'subjects': ['English', 'Kiswahili', 'History', 'Geography', 'CRE', 'IRE', 'HRE'], 'min_grade': 'C+'},
                    'Subject2': {'subjects': ['English', 'Kiswahili', 'History', 'Geography', 'CRE', 'IRE', 'HRE'], 'min_grade': 'C+'},
                    'Subject3': {'subjects': ['English', 'Kiswahili', 'History', 'Geography', 'CRE', 'IRE', 'HRE'], 'min_grade': 'C+'},
                    'Subject4': {'subjects': ['Mathematics', 'Biology', 'Physics', 'Chemistry', 'Business Studies', 'Computer Studies', 'Agriculture', 'Home Science', 'Art & Design', 'Music', 'French', 'German'], 'min_grade': 'C+'}
                },
                'skills': ['creative', 'communication', 'analytical', 'research', 'empathy', 'critical_thinking'],
                'interests': ['arts', 'media', 'culture', 'society', 'communication', 'design', 'psychology']
            },
            
            # CLUSTER 4 - GEOSCIENCES
            4: {
                'name': 'Geosciences & Related',
                'programmes': [
                    'Bachelor of Science (Geospatial Engineering)', 'Bachelor of Science (Geophysical and Mineralogy)',
                    'Bachelor of Science (Earth Science, With IT)', 'Bachelor of Science (Meteorology)',
                    'Bachelor of Science (Geology)', 'Bachelor of Science (Astronomy and Astrophysics)',
                    'Bachelor of Science (Geophysics)', 'Bachelor of Science (Geospatial Information Science, With IT)',
                    'Bachelor of Technology (Geospatial Engineering Technology)', 'Bachelor of Technology (Geoinformation Technology)',
                    'Bachelor of Science (Geospatial Information Science)', 'Bachelor of Science in Geospatial Information Science',
                    'Bachelor of Engineering (Geospatial Engineering)', 'Bachelor of Science (Spatial Management)',
                    'Bachelor of Science in Geomatic Engineering and Geospatial Information Systems', 'Bachelor of Science in Mining Physics (Geophysics)',
                    'Bachelor of Science in Geophysics', 'Bachelor of Science (Hydrology and Water Resources Management)',
                    'Bachelor of Science (Geomatic & Geospatial Information Systems)', 'Bachelor of Applied Science (Geo-informatics)',
                    'Bachelor of Science (Geospatial Information Science and Remote Sensing)', 'Bachelor of Science (Geomatic Engineering and Geospatial Information Systems)',
                    'Bachelor of Arts (Geography)', 'Bachelor of Science (Geography)', 'Bachelor of Arts (Geography and Economics)',
                    'Bachelor of Arts (Kiswahili and Geography)', 'Bachelor of Science (Geography and Natural Resource Management, With IT)'
                ],
                'subject_requirements': {
                    'Subject1': {'subjects': ['Mathematics'], 'min_grade': 'C+'},
                    'Subject2': {'subjects': ['Physics'], 'min_grade': 'C+'},
                    'Subject3': {'subjects': ['Biology', 'Chemistry', 'Geography'], 'min_grade': 'C'},
                    'Subject4': {'subjects': ['English', 'Kiswahili', 'History', 'Business Studies', 'Computer Studies', 'Agriculture', 'Home Science'], 'min_grade': 'C+'}
                },
                'skills': ['analytical', 'technical', 'research', 'problem_solving', 'spatial_thinking', 'data_analysis'],
                'interests': ['environment', 'earth_sciences', 'geography', 'research', 'nature', 'maps']
            },
            
            # CLUSTER 5 - ENGINEERING
            5: {
                'name': 'Engineering, Engineering Technology & Related',
                'programmes': [
                    'Bachelor of Engineering (Aeronautical Engineering)', 'Bachelor of Science (Civil and Structural Engineering)',
                    'Bachelor of Engineering (Chemical and Process Engineering)', 'Bachelor of Science in Civil Engineering',
                    'Bachelor of Engineering (Civil & Structural Engineering)', 'Bachelor of Science (Civil Engineering)',
                    'Bachelor of Engineering (Electrical and Electronic Engineering)', 'Bachelor of Engineering (Electrical and Telecommunication Engineering)',
                    'Bachelor of Engineering (Mechanical & Production Engineering)', 'Bachelor of Engineering (Mechanical and Production Engineering)',
                    'Bachelor of Engineering (Mechanical Engineering)', 'Bachelor of Science (Mechatronic Engineering)',
                    'Bachelor of Science (Electrical and Electronics Engineering)', 'Bachelor of Science in Water and Environmental Engineering',
                    'Bachelor of Science (Applications Engineering)', 'Bachelor of Science (Telecommunications and Information Engineering)',
                    'Bachelor of Science in Telecommunications and Information Engineering', 'Bachelor of Science (Control and Instrumentation)',
                    'Bachelor of Science (Instrumentation & Control)', 'Bachelor of Science (Information and Technologies) and Instrumentation',
                    'Bachelor of Science (Instrumentation & Control Engineering)', 'Bachelor of Science (Telecommunications & Information Technology)',
                    'Bachelor of Science (Applications Engineering & Technology)', 'Bachelor of Science (Applied Optics and Lasers)',
                    'Bachelor of Science (Engineering)', 'Bachelor of Science (Engineering Physics)', 'Bachelor of Science in Engineering Physics',
                    'Bachelor of Science (Applied Bioengineering)', 'Bachelor of Science in Applied Bioengineering', 'Bachelor of Science (Biomedical Engineering)',
                    'Bachelor of Science (Agricultural and Biosystems Engineering)', 'Bachelor of Engineering (Mechanical & Bio-systems Engineering)',
                    'Bachelor of Science (Agricultural & Bio-systems Engineering)', 'Bachelor of Science in Agricultural and Biosystems Engineering',
                    'Bachelor of Technology (Civil Engineering Technology)', 'Bachelor of Technology in Electrical and Electronic Engineering',
                    'Bachelor of Technology in Applied Engineering', 'Bachelor of Science (Biomedical Engineering) and Technology',
                    'Bachelor of Science in Renewable Energy and Technology', 'Bachelor of Technology in Renewable Energy and Technology',
                    'Bachelor of Technology in Renewable Energy & Environmental Physics', 'Bachelor of Science (Electrical and Communication Engineering)',
                    'Bachelor of Science (Electronic and Computer Engineering)', 'Bachelor of Science in Electronic and Computer Engineering',
                    'Bachelor of Science (Mechanical and Industrial Engineering)', 'Bachelor of Science (Mechanical & Manufacturing Engineering)',
                    'Bachelor of Science in Mechanical Engineering', 'Bachelor of Science (Mechanical Engineering)',
                    'Bachelor of Engineering (Industrial and Tensile Engineering)', 'Bachelor of Science (Electrical and Electronic Engineering)',
                    'Bachelor of Science (Aeronomic Engineering)', 'Bachelor of Engineering (Chemical Engineering)',
                    'Bachelor of Science (Marine Engineering)', 'Bachelor of Science in Marine Engineering',
                    'Bachelor of Science (Petroleum Engineering)', 'Bachelor of Science in Mining and Mineral Process Engineering'
                ],
                'subject_requirements': {
                    'Subject1': {'subjects': ['Mathematics'], 'min_grade': 'C+'},
                    'Subject2': {'subjects': ['Physics'], 'min_grade': 'C+'},
                    'Subject3': {'subjects': ['Chemistry'], 'min_grade': 'C+'},
                    'Subject4': {'subjects': ['English', 'Kiswahili'], 'min_grade': 'C+'}
                },
                'skills': ['problem_solving', 'technical', 'analytical', 'mathematics', 'design', 'innovation'],
                'interests': ['technology', 'engineering', 'innovation', 'design', 'construction', 'electronics']
            },
            
            # CLUSTER 6 - ARCHITECTURE & CONSTRUCTION
            6: {
                'name': 'Architecture, Building Construction & Related',
                'programmes': [
                    'Bachelor of Architectural Studies/Bachelor of Architecture', 'Bachelor of Architecture',
                    'Bachelor of Quantity Surveying', 'Bachelor of Science (Quantity Surveying)',
                    'Bachelor of Architectural Technology', 'Bachelor of Landscape Architecture',
                    'Bachelor of Real Estate', 'Bachelor of Science (Real Estate)',
                    'Bachelor of Technology (Real Estate and Property Management)', 'Bachelor of Science (Land Administration)',
                    'Bachelor of Arts (Planning)', 'Bachelor of Construction Management', 'Bachelor of Arts (Spatial Planning)',
                    'Bachelor of Science (Construction Management)', 'Bachelor of Arts (Design)',
                    'Bachelor of The Built Environment (Construction Management)', 'Bachelor of Technology (Design)',
                    'Bachelor of The Built Environment (Urban and Regional Planning)', 'Bachelor of Technology (Building Construction)',
                    'Bachelor of Arts (Urban and Regional Planning, With IT)', 'Bachelor of Science (Urban Design and Development)'
                ],
                'subject_requirements': {
                    'Subject1': {'subjects': ['Mathematics'], 'min_grade': 'C+'},
                    'Subject2': {'subjects': ['Physics'], 'min_grade': 'C+'},
                    'Subject3': {'subjects': ['History', 'Geography', 'CRE', 'IRE', 'HRE'], 'min_grade': 'C+'},
                    'Subject4': {'subjects': ['English', 'Kiswahili'], 'min_grade': 'C+'}
                },
                'skills': ['design', 'technical', 'spatial_thinking', 'project_management', 'creative', 'mathematics'],
                'interests': ['architecture', 'design', 'construction', 'planning', 'real_estate', 'buildings']
            },
            
            # CLUSTER 7 - COMPUTING & IT
            7: {
                'name': 'Computing, IT & Related',
                'programmes': [
                    'Bachelor of Science (Computer Science)', 'Bachelor of Science (Mathematics & Computer Science)',
                    'Bachelor of Science in Computer Science', 'Bachelor of Science (Mathematics and Computer Science)',
                    'Bachelor of Science (Applied Computer Science)', 'Bachelor of Science in Mathematics & Computer Science',
                    'Bachelor of Science in Applied Computer Science', 'Bachelor of Science (Maths and Computer Science)',
                    'Bachelor of Science in Applied Physics and Computer Science', 'Bachelor of Technology (Computer Technology)',
                    'Bachelor of Science (Computer Security and Forensics)', 'Bachelor of Science in Computer Information Systems',
                    'Bachelor of Science in Computer Security and Forensics', 'Bachelor of Science in Software Engineering',
                    'Bachelor of Science in Statistics & Computer Science', 'Bachelor of Science (Computer Technology)',
                    'Bachelor of Technology (Communication and Computer Networks)', 'Bachelor of Science (Information Technology)',
                    'Bachelor of Technology (Information Technology)', 'Bachelor of Technology in Information Technology',
                    'Bachelor of Science (Information and Communication Technology)', 'Bachelor of Technology in Information & Communication Technology',
                    'Bachelor of Information Technology', 'Bachelor of Science (Applied Statistics With Computing)',
                    'Bachelor of Science in Applied Statistics With Computing', 'Bachelor of Science (Mathematics and Computing)',
                    'Bachelor of Science (Statistics & Programming)', 'Bachelor of Science (Informatics)',
                    'Bachelor of Science (Biometry and Informatics)', 'Bachelor of Science (Applied Statistics With Programming)',
                    'Bachelor of Science in Statistics and Programming', 'Bachelor of Science (Informatics and Mathematics)',
                    'Bachelor of Science (Business Computing)', 'Bachelor of Science in Business Computing',
                    'Bachelor of Science in Informatics', 'Bachelor of Science in Computer Technology',
                    'Bachelor of Applied Computer Science'
                ],
                'subject_requirements': {
                    'Subject1': {'subjects': ['Mathematics'], 'min_grade': 'C+'},
                    'Subject2': {'subjects': ['Physics'], 'min_grade': 'C+'},
                    'Subject3': {'subjects': ['English', 'Kiswahili', 'History', 'Geography', 'CRE', 'IRE', 'HRE'], 'min_grade': 'C+'},
                    'Subject4': {'subjects': ['English', 'Kiswahili'], 'min_grade': 'C'}
                },
                'skills': ['technical', 'analytical', 'problem_solving', 'programming', 'logic', 'mathematics'],
                'interests': ['technology', 'computers', 'programming', 'innovation', 'problem_solving', 'data']
            },
            
            # CLUSTER 8 - AGRIBUSINESS
            8: {
                'name': 'Agribusiness & Related',
                'programmes': [
                    'Bachelor of Science (Agribusiness)', 'Bachelor of Science (Agricultural Economics & Resource Management)',
                    'Bachelor of Agribusiness Management', 'Bachelor of Science (Agricultural Economics, With IT)',
                    'Bachelor of Science (Agribusiness Management)', 'Bachelor of Science (Agribusiness Economics and Food Industry Management)',
                    'Bachelor of Science Agribusiness Management', 'Bachelor of Science in Agricultural Economics',
                    'Bachelor of Science in Agricultural Resource Management', 'Bachelor of Science (Agribusiness Management, With IT)',
                    'Bachelor of Science (Agricultural Economics and Rural Development)', 'Bachelor of Science in Agricultural Economics and Rural Development',
                    'Bachelor of Science (Agricultural Economics and Resource Management)', 'Bachelor of Science (Agricultural Economics)',
                    'Bachelor of Science (Agricultural Resource Management)', 'Bachelor of Science in Agribusiness Management and Marketing',
                    'Bachelor of Science in Agribusiness Management', 'Bachelor of Science in Agricultural Resource Economics and Management',
                    'Bachelor of Science Agribusiness Management and Enterprise Development', 'Bachelor of Science (Agri Business Management)',
                    'Bachelor of Science (Agribusiness Management & Trade)', 'Bachelor of Science in Agribusiness Management and Trade'
                ],
                'subject_requirements': {
                    'Subject1': {'subjects': ['Mathematics'], 'min_grade': 'C'},
                    'Subject2': {'subjects': ['Biology'], 'min_grade': 'C'},
                    'Subject3': {'subjects': ['Chemistry', 'Physics', 'Agriculture'], 'min_grade': 'C'},
                    'Subject4': {'subjects': ['English', 'Kiswahili', 'History', 'Geography', 'Business Studies', 'Computer Studies', 'Home Science'], 'min_grade': 'C+'}
                },
                'skills': ['analytical', 'business', 'agricultural', 'management', 'entrepreneurship', 'problem_solving'],
                'interests': ['agriculture', 'business', 'economics', 'farming', 'management', 'rural_development']
            },
            
            # CLUSTER 9 - GENERAL SCIENCES
            9: {
                'name': 'General Science, Biological Sciences, Physics, Chemistry & Related',
                'programmes': [
                    'Bachelor of Science', 'Bachelor of Science (Basic Science, With IT)', 'Bachelor of Science (B.sc)',
                    'Bachelor of Science in Biology', 'Bachelor of Science (Cellular and Molecular Biology)',
                    'Bachelor of Science (Biological Sciences)', 'Bachelor of Science (Molecular & Cellular Biology)',
                    'Bachelor of Science (Microbiology and Biotechnology)', 'Bachelor of Science (Conservation Biology)',
                    'Bachelor of Science in Microbiology and Biotechnology', 'Bachelor of Science (Genomic Sciences)',
                    'Bachelor of Science in Microbiology', 'Bachelor of Science (Forensic Biology)', 'Bachelor of Science (Applied Biology)',
                    'Bachelor of Science in Entomology and Parasitology', 'Bachelor of Science in Applied Biology',
                    'Bachelor of Science in Biotechnology', 'Bachelor of Technology (Applied Biology)', 'Bachelor of Science (Biotechnology)',
                    'Bachelor of Technology in Industrial Microbiology & Biotechnology', 'Bachelor of Science (Botany)',
                    'Bachelor of Science (Biochemistry and Molecular Biology)', 'Bachelor of Science (Chemistry)',
                    'Bachelor of Science in Chemistry', 'Bachelor of Science (Environmental Chemistry)',
                    'Bachelor of Science (Physics)', 'Bachelor of Science in Physics', 'Bachelor of Science (Physics, With IT)',
                    'Bachelor of Technology (Technical and Applied Physics)', 'Bachelor of Technology in Applied Physics (Electronics & Instrumentation)',
                    'Bachelor of Science in Biochemistry', 'Bachelor of Science (Medical Biochemistry)',
                    'Bachelor of Science in Medical Biochemistry', 'Bachelor of Science in Medical Microbiology',
                    'Bachelor of Science in Biochemistry and Molecular Biology', 'Bachelor of Science in Biosciences',
                    'Bachelor of Science (Biochemistry)', 'Bachelor of Science (Microbiology)', 'Bachelor of Science in Genomic Science',
                    'Bachelor of Science in Biology (Botany or Zoology Option)', 'Bachelor of Science (Zoology)',
                    'Bachelor of Science in Zoology', 'Bachelor of Science in Molecular Biology and Forensic Technology',
                    'Bachelor of Science Industrial Biotechnology', 'Bachelor of Technology (Biotechnology)',
                    'Bachelor of Science in Biotechnology and Biosafety', 'Bachelor of Science (Forensic Science)',
                    'Bachelor of Science (Analytical Chemistry with Management)', 'Bachelor of Science (Analytical Chemistry)',
                    'Bachelor of Science in Analytical Chemistry with Computing', 'Bachelor of Science (Computer Science, Physical and Optics Options)',
                    'Bachelor of Technology in Applied Chemistry (Analytical & Industrial Options)', 'Bachelor of Science (Industrial Chemistry With Management)',
                    'Bachelor of Science (Industrial Chemistry, With IT)', 'Bachelor of Science (Industrial Chemistry)',
                    'Bachelor of Technology (Industrial and Applied Chemistry)'
                ],
                'subject_requirements': {
                    'Subject1': {'subjects': ['Mathematics'], 'min_grade': 'C'},
                    'Subject2': {'subjects': ['Biology', 'Physics', 'Chemistry'], 'min_grade': 'C'},
                    'Subject3': {'subjects': ['History', 'Geography', 'CRE', 'IRE', 'HRE'], 'min_grade': 'C'},
                    'Subject4': {'subjects': ['English', 'Kiswahili', 'Business Studies', 'Computer Studies', 'Agriculture', 'Home Science', 'Art & Design', 'Music'], 'min_grade': 'C+'}
                },
                'skills': ['research', 'analytical', 'technical', 'problem_solving', 'laboratory', 'scientific_thinking'],
                'interests': ['science', 'research', 'biology', 'chemistry', 'physics', 'experimentation']
            },
            
            # CLUSTER 10 - ACTUARIAL, MATHEMATICS, ECONOMICS
            10: {
                'name': 'Actuarial Science, Accountancy, Mathematics, Economics, Statistics & Related',
                'programmes': [
                    'Bachelor of Actuarial Science', 'Bachelor of Science (Actuarial Science)', 'Bachelor of Science in Actuarial Science',
                    'Bachelor of Science (Actuarial Science With IT)', 'Bachelor of Science (Mathematics)', 'Bachelor of Science in Mathematics',
                    'Bachelor of Science (Statistics)', 'Bachelor of Science (Applied Statistics, With IT)', 'Bachelor of Science (Applied Statistics)',
                    'Bachelor of Science (Mathematical Sciences, With IT)', 'Bachelor of Science in Applied Statistics',
                    'Bachelor of Science (Mathematics and Economics)', 'Bachelor of Science (Mathematics & Business Studies, With IT)',
                    'Bachelor of Science in Mathematics (Pure Mathematics, Applied Mathematics)', 'Bachelor of Science (Mathematics & Economics, With IT)',
                    'Bachelor of Science (Financial Engineering)', 'Bachelor of Science in Mathematics and Finance',
                    'Bachelor of Science in Finance', 'Bachelor of Science (Operations Research)', 'Bachelor of Science (Finance)',
                    'Bachelor of Economics', 'Bachelor of Arts (Economics & Sociology)', 'Bachelor of Economics & Finance',
                    'Bachelor of Science in Economics', 'Bachelor of Arts (Economics, With IT)', 'Bachelor of Science (Economics and Statistics)',
                    'Bachelor of Arts (Economics and Sociology)', 'Bachelor of Science in Economics & Statistics',
                    'Bachelor of Economics & Statistics', 'Bachelor of Arts (Economics)', 'Bachelor of Economics (Economics & Finance, With IT)',
                    'Bachelor of Economics and Finance', 'Bachelor of Science (Accountancy)', 'Bachelor of Science (Financial Engineering)',
                    'Bachelor of Science in Financial Economics', 'Bachelor of Science (Industrial Mathematics)',
                    'Bachelor of Arts (History and Economics)', 'Bachelor of Science in Mathematics and Economics',
                    'Bachelor of Science (Mathematics & Business Studies, With IT)', 'Bachelor of Science in Mathematics and Finance and Statistics)',
                    'Bachelor of Science (Mathematics & Economics, With IT)', 'Bachelor of Arts in Economics',
                    'Bachelor of Arts (History & Economics)'
                ],
                'subject_requirements': {
                    'Subject1': {'subjects': ['Mathematics'], 'min_grade': 'C+'},
                    'Subject2': {'subjects': ['Biology', 'Physics', 'Chemistry'], 'min_grade': 'C+'},
                    'Subject3': {'subjects': ['History', 'Geography', 'CRE', 'IRE', 'HRE'], 'min_grade': 'C+'},
                    'Subject4': {'subjects': ['English', 'Kiswahili'], 'min_grade': 'C+'}
                },
                'skills': ['numeracy', 'analytical', 'problem_solving', 'statistical', 'financial_analysis', 'logical_thinking'],
                'interests': ['mathematics', 'economics', 'finance', 'statistics', 'analysis', 'numbers']
            },
            
            # CLUSTER 11 - DESIGN
            11: {
                'name': 'Interior Design, Fashion Design, Textiles & Related',
                'programmes': [
                    'Bachelor of Arts (Interior Design, With IT)', 'Bachelor of Arts (Textiles, Apparel Design and Fashion Merchandising, With IT)',
                    'Bachelor of Science (Apparel & Fashion Technology)', 'Bachelor of Science (Clothing Textile & Interior Design)',
                    'Bachelor of Science (Fashion Design & Marketing)', 'Bachelor of Science (Fashion Design and Textile Technology)',
                    'Bachelor of Science in Fashion Design and Marketing'
                ],
                'subject_requirements': {
                    'Subject1': {'subjects': ['Chemistry'], 'min_grade': 'C'},
                    'Subject2': {'subjects': ['Mathematics', 'Physics'], 'min_grade': 'C'},
                    'Subject3': {'subjects': ['Biology', 'Home Science'], 'min_grade': 'C'},
                    'Subject4': {'subjects': ['English', 'Kiswahili', 'History', 'Geography', 'Business Studies', 'Computer Studies', 'Agriculture'], 'min_grade': 'C+'}
                },
                'skills': ['creative', 'design', 'technical', 'artistic', 'fashion_sense', 'innovation'],
                'interests': ['fashion', 'design', 'textiles', 'creativity', 'art', 'style']
            },
            
            # CLUSTER 12 - SPORTS SCIENCE
            12: {
                'name': 'Sport Science & Related',
                'programmes': [
                    'Bachelor of Science (Health Promotion and Sports Science)', 'Bachelor of Science (Exercise & Sport Science)',
                    'Bachelor of Science (Recreation and Sports Management)', 'Bachelor of Sports Science & Management',
                    'Bachelor of Sports Management', 'Bachelor of Education (Physical Education and Sports)',
                    'Bachelor of Education (Physical Education)'
                ],
                'subject_requirements': {
                    'Subject1': {'subjects': ['Biology', 'General Science'], 'min_grade': 'C+'},
                    'Subject2': {'subjects': ['Mathematics'], 'min_grade': 'C+'},
                    'Subject3': {'subjects': ['English', 'Kiswahili', 'History', 'Geography', 'CRE', 'IRE', 'HRE'], 'min_grade': 'C+'},
                    'Subject4': {'subjects': ['English', 'Kiswahili', 'Business Studies', 'Computer Studies', 'Agriculture', 'Home Science', 'Art & Design', 'Music'], 'min_grade': 'C+'}
                },
                'skills': ['physical_fitness', 'coaching', 'leadership', 'health_knowledge', 'teamwork', 'communication'],
                'interests': ['sports', 'fitness', 'health', 'coaching', 'physical_activity', 'recreation']
            },
            
            # CLUSTER 13 - MEDICINE & HEALTH
            13: {
                'name': 'Medicine, Health, Veterinary Medicine & Related',
                'programmes': [
                    'Bachelor of Medicine and Bachelor of Surgery (MBChB)',
                    'Bachelor of Dental Surgery',
                    'Bachelor of Pharmacy',
                    'Bachelor of Science in Nursing',
                    'Bachelor of Science in Clinical Medicine',
                    'Bachelor of Science in Medical Laboratory Sciences',
                    'Bachelor of Science in Public Health',
                    'Bachelor of Physiotherapy',
                    'Bachelor of Science in Nutrition and Dietetics',
                    'Bachelor of Veterinary Medicine',
                    'Bachelor of Science (Medical Laboratory Science & Technology)',
                    'Bachelor of Science in Environmental Health',
                    'Bachelor of Science (Food, Nutrition & Dietetics)',
                    'Bachelor of Science in Biomedical Science and Technology'
                ],
                'subject_requirements': {
                    'Subject1': {'subjects': ['Biology'], 'min_grade': 'B'},
                    'Subject2': {'subjects': ['Chemistry'], 'min_grade': 'B'},
                    'Subject3': {'subjects': ['Mathematics', 'Physics'], 'min_grade': 'B'},
                    'Subject4': {'subjects': ['English', 'Kiswahili'], 'min_grade': 'B'}
                },
                'skills': ['empathy', 'analytical', 'problem_solving', 'communication', 'medical_knowledge', 'attention_to_detail'],
                'interests': ['medicine', 'healthcare', 'biology', 'helping_people', 'research', 'science', 'community_service']
            },
            
            # CLUSTER 14 - HISTORY & ARCHAEOLOGY
            14: {
                'name': 'History, Archeology & Related',
                'programmes': [
                    'Bachelor of Arts (History and Archaeology)', 'Bachelor of Arts (History)',
                    'Bachelor of Arts (History and Archaeology, With IT)', 'Bachelor of Arts in History & International Studies'
                ],
                'subject_requirements': {
                    'Subject1': {'subjects': ['History'], 'min_grade': 'C+'},
                    'Subject2': {'subjects': ['English', 'Kiswahili'], 'min_grade': 'C+'},
                    'Subject3': {'subjects': ['Mathematics', 'Biology', 'Physics', 'Chemistry'], 'min_grade': 'C+'},
                    'Subject4': {'subjects': ['Geography', 'CRE', 'IRE', 'HRE', 'Business Studies', 'Computer Studies', 'Agriculture', 'Home Science'], 'min_grade': 'C+'}
                },
                'skills': ['research', 'analytical', 'historical_analysis', 'writing', 'critical_thinking', 'cultural_understanding'],
                'interests': ['history', 'archaeology', 'culture', 'research', 'heritage', 'ancient_civilizations']
            },
            
            # CLUSTER 15 - AGRICULTURE & ENVIRONMENT
            15: {
                'name': 'Agriculture, Animal Health, Food Science, Nutrition Dietetics, Environmental Sciences, Natural Resources & Related',
                'programmes': [
                    'Bachelor of Science (Animal Science & Management)', 'Bachelor of Science (Animal Science, With IT)',
                    'Bachelor of Science in Animal Science', 'Bachelor of Science in Animal Science & Technology',
                    'Bachelor of Science in Animal Products Technology', 'Bachelor of Science (Animal Health & Production)',
                    'Bachelor of Science (Animal Health and Production)', 'Bachelor of Science (Animal Health, Production & Processing)',
                    'Bachelor of Science (Animal Production & Health Management)', 'Bachelor of Science in Animal Health Management',
                    'Bachelor of Science in Animal Production', 'Bachelor of Science in Applied Animal Laboratory Science',
                    'Bachelor of Science (Food Nutrition and Dietetics)', 'Bachelor of Science (Human Nutrition and Dietetics)',
                    'Bachelor of Environmental Science', 'Bachelor of Environmental Studies', 'Bachelor of Science in Environmental Studies',
                    'Bachelor of Environmental Studies (Arts)', 'Bachelor of Environmental Studies (Science)',
                    'Bachelor of Science in Environmental Science', 'Bachelor of Environmental Education',
                    'Bachelor of Science (Climate Change and Development, With IT)', 'Bachelor of Science (Crop Improvement & Protection)',
                    'Bachelor of Science (Waste Management)', 'Bachelor of Science (Water Resource Management)',
                    'Bachelor of Science in Ethno botany', 'Bachelor of Science (Agriculture & Human Ecology Extension)',
                    'Bachelor of Science (Agriculture and Enterprise Development)', 'Bachelor of Science (Dairy Technology & Management)',
                    'Bachelor of Science (Leather Technology)', 'Bachelor of Science (Soil Science)',
                    'Bachelor of Science (Soils & Land Use Management)', 'Bachelor of Science (Water and Environment Management)',
                    'Bachelor of Science (Wood Science and Industrial Processes)', 'Bachelor of Science (Soil Science, With IT)',
                    'Bachelor of Science (Wildlife Management)', 'Bachelor of Science (Agricultural Biotechnology)',
                    'Bachelor of Science (Horticultural Science & Management)', 'Bachelor of Science (Horticulture, With IT)',
                    'Bachelor of Science (Range Management)', 'Bachelor of Science (Bio-resources Management and Conservation)',
                    'Bachelor of Science (Integrated Forest Resources Management)', 'Bachelor of Science (Natural Products)',
                    'Bachelor of Science in Agriculture', 'Bachelor of Science (Natural Resources Management)',
                    'Bachelor of Science (Environmental Horticulture & Landscaping Technology)', 'Bachelor of Science (Forestry)',
                    'Bachelor of Science (Horticulture)', 'Bachelor of Science in Horticulture',
                    'Bachelor of Science in Horticultural Science & Management', 'Bachelor of Science (Wildlife Enterprises & Management)',
                    'Bachelor of Science in Wildlife Enterprise & Management', 'Bachelor of Science (Dryland, Agriculture & Enterprise Development)',
                    'Bachelor of Science in Natural Resource Management', 'Bachelor of Science (Dryland Animal Science)',
                    'Bachelor of Science in Soil Environment & Land Use Management)', 'Bachelor of Science (Seed Science & Technology)',
                    'Bachelor of Science (Nutraceutical Science and Technology)', 'Bachelor of Science (Agroforestry & Rural Development)',
                    'Bachelor of Science in Nutraceutical Science and Technology', 'Bachelor of Science (Aquatic Resources Conservation and Development, With IT)',
                    'Bachelor of Science (Utilization & Sustainability of Arid Lands (Usal))', 'Bachelor of Technology (Environmental Resource Management)',
                    'Bachelor of Science (Environmental Management)', 'Bachelor of Science (Environmental Science, With IT)',
                    'Bachelor of Science (Environmental Science)', 'Bachelor of Science in Environmental Science and Technology',
                    'Bachelor of Science (Environmental Sciences)', 'Bachelor of Environmental Studies (Community Development)',
                    'Bachelor of Science (Agriculture and Biotechnology)', 'Bachelor of Environmental Planning & Development Management',
                    'Bachelor of Environmental Studies and Community Development', 'Bachelor of Science in Environment, Lands and Sustainable Development',
                    'Bachelor of Science in Natural Resources', 'Bachelor of Science (Sustainable Energy & Climate Change Systems)',
                    'Bachelor of Environmental (Environmental Resource Conservation)', 'Bachelor of Science (Food Processing Technology)',
                    'Bachelor of Science in Food Science & Technology', 'Bachelor of Science (Food Science & Technology)',
                    'Bachelor of Science (Food Science and Management)', 'Bachelor of Science (Food Security)',
                    'Bachelor of Science in Food Technology & Quality Assurance', 'Bachelor of Science (Applied Aquatic Science)',
                    'Bachelor of Science (Fisheries & Aquatic Sciences)', 'Bachelor of Science in Aquaculture and Fisheries Technology',
                    'Bachelor of Science in Fisheries and Oceanography', 'Bachelor of Science in Marine Resource Management',
                    'Bachelor of Science (Coastal & Marine Resource Management)', 'Bachelor of Science (Marine Biology & Fisheries)',
                    'Bachelor of Science (Fisheries and Aquaculture Management)', 'Bachelor of Science (Fisheries and Aquaculture, With IT)',
                    'Bachelor of Science Fisheries Management and Aquaculture Technology', 'Bachelor of Science in Fisheries and Aquaculture',
                    'Bachelor of Science in Water and Environment Management', 'Bachelor of Science (Dryland Agriculture)',
                    'Bachelor of Science (Land Resource Management)', 'Bachelor of Science (Agriculture)'
                ],
                'subject_requirements': {
                    'Subject1': {'subjects': ['Biology'], 'min_grade': 'C+'},
                    'Subject2': {'subjects': ['Chemistry'], 'min_grade': 'C+'},
                    'Subject3': {'subjects': ['Mathematics', 'Physics', 'Geography'], 'min_grade': 'C+'},
                    'Subject4': {'subjects': ['English', 'Kiswahili'], 'min_grade': 'C+'}
                },
                'skills': ['agricultural', 'environmental', 'analytical', 'research', 'sustainability', 'problem_solving'],
                'interests': ['agriculture', 'environment', 'animals', 'farming', 'conservation', 'sustainability']
            },
            
            # CLUSTER 16 - GEOGRAPHY
            16: {
                'name': 'Geography & Related',
                'programmes': [
                    'Bachelor of Arts (Geography)', 'Bachelor of Science (Geography)',
                    'Bachelor of Arts (Geography and Economics)', 'Bachelor of Arts (Kiswahili and Geography)',
                    'Bachelor of Science (Geography and Natural Resource Management, With IT)',
                    'Bachelor of Science (Environmental Conservation and Natural Resources Management)',
                    'Bachelor of Science (Land Resource Planning & Management)', 'Bachelor of Science in Land Resource Planning & Management'
                ],
                'subject_requirements': {
                    'Subject1': {'subjects': ['Geography'], 'min_grade': 'C+'},
                    'Subject2': {'subjects': ['Mathematics'], 'min_grade': 'C+'},
                    'Subject3': {'subjects': ['Biology', 'Physics', 'Chemistry'], 'min_grade': 'C+'},
                    'Subject4': {'subjects': ['English', 'Kiswahili', 'History', 'Business Studies', 'Computer Studies', 'Agriculture', 'Home Science'], 'min_grade': 'C+'}
                },
                'skills': ['spatial_thinking', 'analytical', 'research', 'environmental', 'mapping', 'data_analysis'],
                'interests': ['geography', 'environment', 'maps', 'spatial_analysis', 'nature', 'conservation']
            },
            
            # CLUSTER 17 - LANGUAGES
            17: {
                'name': 'French & German',
                'programmes': [
                    'Bachelor of Arts (French)', 'Bachelor of Arts (French, With IT)', 'Bachelor of Arts (German)',
                    'Bachelor of Education (French)', 'Bachelor of Education (French, With IT)', 'Bachelor of Education (German)',
                    'Bachelor of Education (Arts) German'
                ],
                'subject_requirements': {
                    'Subject1': {'subjects': ['French', 'German'], 'min_grade': 'C+'},
                    'Subject2': {'subjects': ['English', 'Kiswahili'], 'min_grade': 'C+'},
                    'Subject3': {'subjects': ['Mathematics', 'Biology', 'Physics', 'Chemistry', 'History', 'Geography', 'CRE', 'IRE', 'HRE'], 'min_grade': 'C+'},
                    'Subject4': {'subjects': ['Business Studies', 'Computer Studies', 'Agriculture', 'Home Science', 'Art & Design', 'Music'], 'min_grade': 'C+'}
                },
                'skills': ['linguistic', 'communication', 'cultural_understanding', 'translation', 'analytical', 'writing'],
                'interests': ['languages', 'culture', 'communication', 'translation', 'literature', 'international_relations']
            },
            
            # CLUSTER 18 - MUSIC
            18: {
                'name': 'Music & Related',
                'programmes': [
                    'Bachelor of Arts (Music)', 'Bachelor of Arts (Music, With IT)', 'Bachelor of Music',
                    'Bachelor of Music (Technology)', 'Bachelor of Education (Music)', 'Bachelor of Education (Music, With IT)'
                ],
                'subject_requirements': {
                    'Subject1': {'subjects': ['Music'], 'min_grade': 'C+'},
                    'Subject2': {'subjects': ['English', 'Kiswahili'], 'min_grade': 'C+'},
                    'Subject3': {'subjects': ['Mathematics', 'Biology', 'Physics', 'Chemistry', 'History', 'Geography', 'CRE', 'IRE', 'HRE'], 'min_grade': 'C+'},
                    'Subject4': {'subjects': ['Business Studies', 'Computer Studies', 'Agriculture', 'Home Science', 'Art & Design', 'French', 'German'], 'min_grade': 'C+'}
                },
                'skills': ['musical', 'creative', 'performance', 'composition', 'technical', 'artistic'],
                'interests': ['music', 'performance', 'composition', 'arts', 'creativity', 'entertainment']
            },
            
            # CLUSTER 19 - EDUCATION
            19: {
                'name': 'Education & Related',
                'programmes': [
                    'Bachelor of Education (Arts)', 'Bachelor of Education (Early Childhood Development Education)',
                    'Bachelor of Education (Early Childhood Development)', 'Bachelor of Education (Early Childhood Education)',
                    'Bachelor of Education (Early Childhood Education, With IT)', 'Bachelor of Education (Early Childhood)',
                    'Bachelor of Education in Early Childhood Education', 'Bachelor of Education (Library Science)',
                    'Bachelor of Education (Early Childhood and Primary Education)', 'Bachelor of Arts (With Education)',
                    'Bachelor of Education (Science)', 'Bachelor of Education (Science,With IT)', 'Bachelor of Education (Science with IT)',
                    'Bachelor of Education (Arts) With Guidance and Counselling', 'Bachelor of Education (Arts, With IT)',
                    'Bachelor of Education (Home Science and Technology)', 'Bachelor of Education (Guidance and Counselling)',
                    'Bachelor of Education Arts (Home Economics)', 'Bachelor of Education (Agricultural Education)',
                    'Bachelor of Science in Agricultural Education & Extension', 'Bachelor of Science (Agricultural Education and Extension)',
                    'Bachelor of Education (Computer Studies)', 'Bachelor of Education (ICT)', 'Bachelor of Education (Agriculture)',
                    'Bachelor of Agricultural Education & Extension', 'Bachelor of Agricultural Education and Extension',
                    'Bachelor of Science in Agricultural Extension', 'Bachelor of Science (Agriculture Education and Extension)',
                    'Bachelor of Science Agricultural Extension and Education', 'Bachelor of Science (Agricultural Extension Education)',
                    'Bachelor of Science (Agricultural Education & Extension)', 'Bachelor of Science (Agricultural Extension and Education)',
                    'Bachelor of Science (Agriculture Education & Extension)', 'Bachelor of Science (Agriculture Education and Extension, With IT)',
                    'Bachelor of Education Arts(Business Studies)', 'Bachelor of Education (Physical Education and Sports)',
                    'Bachelor of Education (Physical Education)', 'Bachelor of Education (Special Needs Education - Secondary Option)',
                    'Bachelor of Education (Special Needs Education)', 'Bachelor of Education (Visual and Performing Arts)',
                    'Bachelor of Science with Education', 'Bachelor of Education (Technical and Vocational Education)',
                    'Bachelor of Education (Technology)', 'Bachelor of Education (Technology Education)'
                ],
                'subject_requirements': {
                    'Subject1': {'subjects': ['English', 'Kiswahili', 'Mathematics', 'History', 'Geography', 'CRE', 'IRE', 'HRE', 'Social Studies', 'Home Science', 'Art & Design', 'Computer Studies', 'Music', 'French', 'German'], 'min_grade': 'C+'},
                    'Subject2': {'subjects': ['English', 'Kiswahili', 'Mathematics', 'History', 'Geography', 'CRE', 'IRE', 'HRE', 'Social Studies', 'Home Science', 'Art & Design', 'Computer Studies', 'Music', 'French', 'German'], 'min_grade': 'C+'},
                    'Subject3': {'subjects': ['Biology', 'Physics', 'Chemistry', 'Business Studies', 'Agriculture'], 'min_grade': 'C+'},
                    'Subject4': {'subjects': ['Biology', 'Physics', 'Chemistry', 'Business Studies', 'Agriculture'], 'min_grade': 'C+'}
                },
                'skills': ['teaching', 'communication', 'patience', 'leadership', 'organization', 'subject_expertise'],
                'interests': ['education', 'teaching', 'mentoring', 'children', 'learning', 'community_development']
            },
            
            # CLUSTER 20 - RELIGIOUS STUDIES
            20: {
                'name': 'Religious Studies, Theology, Islamic Studies & Related',
                'programmes': [
                    'Bachelor of Arts (Religion, With IT)', 'Bachelor of Arts in Sociology and Religious Studies',
                    'Bachelor of Arts (Religious Studies)', 'Bachelor of Arts (Theology, With IT)',
                    'Bachelor of Arts (Sociology & Religion)', 'Bachelor of Theology',
                    'Bachelor of Arts in Intercultural Studies', 'Bachelor of Arts in Biblical Studies',
                    'Bachelor of Arts in Islamic Studies', 'Bachelor of Arts in Church Education Ministries',
                    'Bachelor of Arts in Islamic Sharia', 'Bachelor of Arts in Christian Ministries'
                ],
                'subject_requirements': {
                    'Subject1': {'subjects': ['CRE', 'IRE', 'HRE'], 'min_grade': 'C+'},
                    'Subject2': {'subjects': ['English', 'Kiswahili'], 'min_grade': 'C'},
                    'Subject3': {'subjects': ['History', 'Geography'], 'min_grade': 'C+'},
                    'Subject4': {'subjects': ['Mathematics', 'Biology', 'Physics', 'Chemistry', 'Business Studies', 'Computer Studies', 'Agriculture', 'Home Science'], 'min_grade': 'C+'}
                },
                'skills': ['theological', 'communication', 'counseling', 'leadership', 'research', 'ethical_reasoning'],
                'interests': ['religion', 'theology', 'spirituality', 'philosophy', 'community_service', 'counseling']
            }
        }
    
    def parse_grade_requirement(self, grade_text):
        """Parse grade requirements like 'C+', 'C (PLAIN)', 'B (PLAIN)'"""
        if grade_text == "C++":
            return "C+"
        if 'PLAIN' in grade_text:
            return grade_text.split('(')[0].strip()
        return grade_text.strip()
    
    def meets_subject_requirements(self, user_subjects, cluster_requirements):
        """Check if user meets subject requirements for a cluster"""
        user_subjects_clean = {subject: grade for subject, grade in user_subjects.items() 
                              if grade not in ["Not Taken", "Select Grade"]}
        
        missing_requirements = []
        
        for req_key, requirement in cluster_requirements.items():
            requirement_met = False
            required_grade = self.parse_grade_requirement(requirement['min_grade'])
            required_points = self.grade_to_points(required_grade)
            
            for subject_option in requirement['subjects']:
                mapped_subject = self.subject_mapping.get(subject_option, subject_option)
                
                user_grade = user_subjects_clean.get(mapped_subject, "Not Taken")
                if user_grade != "Not Taken" and self.grade_to_points(user_grade) >= required_points:
                    requirement_met = True
                    break
            
            if not requirement_met:
                subject_names = [self.subject_mapping.get(sub, sub) for sub in requirement['subjects']]
                missing_requirements.append({
                    'requirement': req_key,
                    'required_subjects': subject_names,
                    'required_grade': required_grade
                })
        
        if missing_requirements:
            return False, missing_requirements
        
        return True, []

    def calculate_cluster_match_score(self, user_subjects, user_skills, user_interests, cluster_id):
        """Calculate how well user matches a cluster with 60% weight for interests/skills"""
        cluster = self.kuccps_clusters[cluster_id]
        
        # Subject match (40% weight)
        subject_requirements_met, missing_reqs = self.meets_subject_requirements(user_subjects, cluster['subject_requirements'])
        subject_score = 100 if subject_requirements_met else 0
        
        # Skills match (30% weight)
        cluster_skills = cluster['skills']
        skills_match = self.calculate_enhanced_skills_match(user_skills, cluster_skills)
        
        # Interests match (30% weight)
        cluster_interests = cluster['interests']
        interests_match = self.calculate_enhanced_interests_match(user_interests, cluster_interests)
        
        # Calculate overall score with 60% for interests/skills and 40% for subjects
        overall_score = (subject_score * 0.4) + (skills_match * 0.3) + (interests_match * 0.3)
        
        # Strong bonus for medical interests matching medical clusters
        if cluster_id == 13 and 'Medicine' in user_interests:
            overall_score = min(overall_score * 1.3, 100)  # 30% bonus for medical interests
        
        return {
            'cluster_id': cluster_id,
            'cluster_name': cluster['name'],
            'match_score': round(overall_score, 1),
            'subject_score': subject_score,
            'skills_match': round(skills_match, 1),
            'interests_match': round(interests_match, 1),
            'missing_requirements': missing_reqs,
            'eligible_programmes': cluster['programmes'][:5] if subject_requirements_met else [],
            'total_programmes': len(cluster['programmes']),
            'requirements_met': subject_requirements_met
        }
    
    def grade_to_points(self, grade):
        """Convert grade to numerical points"""
        return self.grade_points.get(grade, 0)
    
    def calculate_enhanced_skills_match(self, user_skills, cluster_skills):
        """Calculate enhanced skills similarity with better matching"""
        if not user_skills or not cluster_skills:
            return 0
        
        user_skills_set = set(skill.lower().replace(' ', '_') for skill in user_skills)
        cluster_skills_set = set(cluster_skills)
        
        if len(cluster_skills_set) == 0:
            return 0
            
        intersection = user_skills_set.intersection(cluster_skills_set)
        
        # Calculate base match
        base_match = (len(intersection) / len(cluster_skills_set)) * 100
        
        # Bonus for critical skills matches
        critical_skills = ['analytical', 'problem_solving', 'research', 'communication']
        critical_matches = len(intersection.intersection(set(critical_skills)))
        
        return min(base_match + (critical_matches * 10), 100)
    
    def calculate_enhanced_interests_match(self, user_interests, cluster_interests):
        """Calculate enhanced interests similarity with expanded mappings"""
        if not user_interests or not cluster_interests:
            return 50  # Neutral score instead of 0
        
        user_interests_set = set(user_interests)
        cluster_interests_set = set(cluster_interests)
        
        if len(cluster_interests_set) == 0:
            return 50
            
        # Direct matches
        direct_intersection = user_interests_set.intersection(cluster_interests_set)
        direct_match = len(direct_intersection) / len(cluster_interests_set)
        
        # Expanded matches through interest mappings
        expanded_matches = 0
        for user_interest in user_interests_set:
            if user_interest in self.enhanced_interest_mappings:
                mapped_interests = self.enhanced_interest_mappings[user_interest]
                for mapped_interest in mapped_interests:
                    if mapped_interest in cluster_interests_set:
                        expanded_matches += 0.5  # Partial credit for mapped matches
        
        # Strong bonus for medical interests in medical clusters
        medical_bonus = 0
        if 'Medicine' in user_interests_set and 'medicine' in cluster_interests_set:
            medical_bonus = 30
        
        total_match = (direct_match * 70) + (expanded_matches * 10) + medical_bonus
        
        return min(total_match, 100)
    
    def generate_recommendations(self, subjects_grades, skills_interests):
        """Generate career recommendations with 60% weight for interests/skills"""
        user_subjects = {subject: grade for subject, grade in subjects_grades.items() 
                        if grade not in ["Not Taken", "Select Grade"]}
        user_skills = skills_interests.get('skills', [])
        user_interests = skills_interests.get('interests', [])
        
        recommendations = []
        
        for cluster_id in self.kuccps_clusters.keys():
            cluster_match = self.calculate_cluster_match_score(
                user_subjects, user_skills, user_interests, cluster_id
            )
            
            # Include clusters even with partial matches due to high interest/skill weights
            if cluster_match['match_score'] >= 40:  # Lower threshold to show more options
                for programme in cluster_match['eligible_programmes']:
                    recommendations.append({
                        'career': programme,
                        'cluster': f"Cluster {cluster_id}: {cluster_match['cluster_name']}",
                        'match_score': cluster_match['match_score'],
                        'subject_match': cluster_match['subject_score'],
                        'skills_match': cluster_match['skills_match'],
                        'interests_match': cluster_match['interests_match'],
                        'description': f"Degree programme in {cluster_match['cluster_name']}",
                        'recommended_courses': [programme],
                        'universities': ["Various Kenyan Universities"],
                        'reasoning': self.generate_reasoning(cluster_match, user_interests),
                        'required_subjects': self.get_required_subjects_list(cluster_id),
                        'required_grades': self.get_required_grades_dict(cluster_id),
                        'missing_requirements': cluster_match['missing_requirements']
                    })
        
        # Sort by match score (now heavily weighted towards interests/skills)
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        
        return {
            'top_careers': recommendations[:15],  # Show more recommendations
            'all_careers': recommendations,
            'user_profile': {
                'subjects_count': len(user_subjects),
                'skills_count': len(user_skills),
                'interests_count': len(user_interests),
                'primary_interest': user_interests[0] if user_interests else "Not specified"
            }
        }
    
    def generate_reasoning(self, cluster_match, user_interests):
        """Generate reasoning based on match scores"""
        reasoning = []
        
        if cluster_match['interests_match'] >= 80:
            reasoning.append("Excellent interest alignment")
        elif cluster_match['interests_match'] >= 60:
            reasoning.append("Strong interest match")
        
        if cluster_match['skills_match'] >= 80:
            reasoning.append("Skills perfectly match career requirements")
        elif cluster_match['skills_match'] >= 60:
            reasoning.append("Good skills alignment")
        
        if cluster_match['requirements_met']:
            reasoning.append("Meets all academic requirements")
        else:
            reasoning.append("Consider improving specific subjects")
            
        # Special reasoning for medical interests
        if 'Medicine' in user_interests and cluster_match['cluster_id'] == 13:
            reasoning.append("Perfect match for medical career aspirations")
        
        return "; ".join(reasoning)
    
    def get_required_subjects_list(self, cluster_id):
        """Get list of required subjects for a cluster"""
        cluster = self.kuccps_clusters[cluster_id]
        required_subjects = set()
        
        for requirement in cluster['subject_requirements'].values():
            for subject in requirement['subjects']:
                mapped_subject = self.subject_mapping.get(subject, subject)
                required_subjects.add(mapped_subject)
        
        return list(required_subjects)
    
    def get_required_grades_dict(self, cluster_id):
        """Get required grades for subjects in a cluster"""
        cluster = self.kuccps_clusters[cluster_id]
        required_grades = {}
        
        for req_key, requirement in cluster['subject_requirements'].items():
            for subject in requirement['subjects']:
                mapped_subject = self.subject_mapping.get(subject, subject)
                grade = requirement['min_grade']
                if grade == "C++":
                    grade = "C+"
                required_grades[mapped_subject] = grade
        
        return required_grades
    
    def get_career_insights(self, recommendations):
        """Generate insights about the career recommendations"""
        insights = []
        
        if not recommendations['top_careers']:
            insights.append("❌ You don't currently meet the subject requirements for any KUCCPS degree clusters.")
            insights.append("💡 Consider improving your grades in core subjects or exploring TVET/diploma options.")
            return insights
        
        top_career = recommendations['top_careers'][0]
        user_profile = recommendations['user_profile']
        
        # Interest-focused insights
        if user_profile['primary_interest']:
            insights.append(f"🎯 Your primary interest in {user_profile['primary_interest']} strongly influenced recommendations")
        
        if top_career['interests_match'] >= 80:
            insights.append("❤️ Excellent interest alignment with top career choices")
        elif top_career['interests_match'] >= 60:
            insights.append("✅ Good interest match with recommended careers")
        
        if top_career['skills_match'] >= 80:
            insights.append("🛠️ Your skills perfectly match career requirements")
        
        # Medical career specific insights
        medical_careers = [career for career in recommendations['top_careers'] 
                          if 'medicine' in career['cluster'].lower() or 'health' in career['cluster'].lower()]
        if medical_careers and user_profile['primary_interest'] == 'Medicine':
            insights.append("🏥 Strong match for medical and healthcare careers based on your interests")
        
        insights.append("📊 Recommendations weighted 60% towards your interests and skills, 40% towards subjects")
        
        return insights

    def get_cluster_recommendations(self, user_subjects, user_skills, user_interests):
        """Get KUCCPS cluster recommendations for user"""
        recommendations = []
        
        for cluster_id in self.kuccps_clusters.keys():
            cluster_match = self.calculate_cluster_match_score(
                user_subjects, user_skills, user_interests, cluster_id
            )
            recommendations.append(cluster_match)
        
        # Sort by match score
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        
        return {
            'top_clusters': [r for r in recommendations if r['match_score'] >= 40][:5],
            'all_clusters': recommendations,
            'user_profile': {
                'subjects_count': len([g for g in user_subjects.values() if g not in ["Not Taken", "Select Grade"]]),
                'skills_count': len(user_skills),
                'interests_count': len(user_interests)
            }
        }