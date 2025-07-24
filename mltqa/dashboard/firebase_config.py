import firebase_admin
from firebase_admin import credentials, storage
import os 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SERVICE_ACCOUNT_PATH = os.path.join(BASE_DIR, "firebase.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'mltqa-9864c.firebasestorage.app' 
    })
    

bucket = storage.bucket()
