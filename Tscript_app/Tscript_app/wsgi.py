"""
WSGI config for Tscript_app project.
"""

import os
from django.core.wsgi import get_wsgi_application
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
env_path = BASE_DIR.parent / '.env'
load_dotenv(env_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tscript_app.settings')

application = get_wsgi_application()
