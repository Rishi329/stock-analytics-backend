import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Firebase Configuration
    FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID', 'stock-analytics-7f387')
    FIREBASE_PRIVATE_KEY_ID = os.getenv('FIREBASE_PRIVATE_KEY_ID')
    FIREBASE_PRIVATE_KEY = os.getenv('FIREBASE_PRIVATE_KEY', '').replace('\\n', '\n')
    FIREBASE_CLIENT_EMAIL = os.getenv('FIREBASE_CLIENT_EMAIL')
    FIREBASE_CLIENT_ID = os.getenv('FIREBASE_CLIENT_ID')
    FIREBASE_AUTH_URI = os.getenv('FIREBASE_AUTH_URI', 'https://accounts.google.com/o/oauth2/auth')
    FIREBASE_TOKEN_URI = os.getenv('FIREBASE_TOKEN_URI', 'https://oauth2.googleapis.com/token')
    FIREBASE_AUTH_PROVIDER_X509_CERT_URL = os.getenv(
        'FIREBASE_AUTH_PROVIDER_X509_CERT_URL',
        'https://www.googleapis.com/oauth2/v1/certs'
    )
    
    # API Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', '8000'))
    
    # Cache Configuration
    CACHE_EXPIRE_SECONDS = int(os.getenv('CACHE_EXPIRE_SECONDS', '300'))
    
    # Development Settings
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'
    
    @classmethod
    def get_firebase_credentials(cls) -> Dict[str, Any]:
        """Get Firebase credentials as a dictionary for Admin SDK initialization"""
        return {
            "type": "service_account",
            "project_id": cls.FIREBASE_PROJECT_ID,
            "private_key_id": cls.FIREBASE_PRIVATE_KEY_ID,
            "private_key": cls.FIREBASE_PRIVATE_KEY,
            "client_email": cls.FIREBASE_CLIENT_EMAIL,
            "client_id": cls.FIREBASE_CLIENT_ID,
            "auth_uri": cls.FIREBASE_AUTH_URI,
            "token_uri": cls.FIREBASE_TOKEN_URI,
            "auth_provider_x509_cert_url": cls.FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
            "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{cls.FIREBASE_CLIENT_EMAIL}"
        }
    
    @classmethod
    def is_firebase_configured(cls) -> bool:
        """Check if Firebase is properly configured"""
        required_fields = [
            cls.FIREBASE_PROJECT_ID,
            cls.FIREBASE_PRIVATE_KEY_ID,
            cls.FIREBASE_PRIVATE_KEY,
            cls.FIREBASE_CLIENT_EMAIL,
            cls.FIREBASE_CLIENT_ID
        ]
        return all(field for field in required_fields)

config = Config()