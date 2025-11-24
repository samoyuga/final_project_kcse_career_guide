"""
Career paths data loader for KCSE Career Guidance Tool
KUCCPS 20 Clusters Version
"""

import json
import os

def load_career_data():
    """Load career paths data from JSON file with KUCCPS 20 clusters"""
    try:
        current_dir = os.path.dirname(__file__)
        json_path = os.path.join(current_dir, 'career_paths.json')
        
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Convert to the format expected by CareerEngine
        career_paths = {}
        for cluster_name, cluster_data in data['career_clusters'].items():
            career_paths[cluster_name] = cluster_data['careers']
        
        return career_paths
        
    except Exception as e:
        print(f"Error loading career data: {e}")
        return get_fallback_data()

def get_career_clusters():
    """Get list of all KUCCPS career clusters"""
    try:
        current_dir = os.path.dirname(__file__)
        json_path = os.path.join(current_dir, 'career_paths.json')
        
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        return data['metadata']['kuccps_clusters']
    except:
        return list(load_career_data().keys())

def get_cluster_info(cluster_name):
    """Get information about a specific career cluster"""
    try:
        current_dir = os.path.dirname(__file__)
        json_path = os.path.join(current_dir, 'career_paths.json')
        
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        cluster_data = data['career_clusters'].get(cluster_name, {})
        return {
            'description': cluster_data.get('description', ''),
            'icon': cluster_data.get('icon', '📁'),
            'career_count': len(cluster_data.get('careers', []))
        }
    except:
        return {'description': '', 'icon': '📁', 'career_count': 0}

def validate_career_data():
    """Validate the career data structure"""
    try:
        data = load_career_data()
        required_fields = ['career', 'required_subjects', 'required_grades', 'skills', 
                          'interests', 'description', 'universities', 'courses']
        
        for cluster, careers in data.items():
            for career in careers:
                for field in required_fields:
                    if field not in career:
                        print(f"Missing field '{field}' in career: {career.get('career', 'Unknown')}")
                        return False
        return True
    except Exception as e:
        print(f"Career data validation error: {e}")
        return False

def get_kuccps_statistics():
    """Get statistics about the KUCCPS career data"""
    try:
        current_dir = os.path.dirname(__file__)
        json_path = os.path.join(current_dir, 'career_paths.json')
        
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        return data['metadata']
    except:
        return {}

def get_fallback_data():
    """Provide fallback data if JSON file fails to load"""
    return {
        "Medicine and Health Sciences": [
            {
                "career": "Medical Doctor",
                "required_subjects": ["Biology", "Chemistry", "Physics"],
                "required_grades": {"Biology": "B+", "Chemistry": "B+", "Physics": "B"},
                "skills": ["Problem Solving", "Critical Thinking", "Communication"],
                "interests": ["Sciences", "Medicine", "Helping People"],
                "description": "Diagnose and treat illnesses",
                "universities": ["University of Nairobi", "Kenyatta University"],
                "courses": ["Bachelor of Medicine and Surgery"]
            }
        ]
    }