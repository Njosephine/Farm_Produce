import os
from django.core.asgi import get_asgi_application

# Set the correct settings module for the project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutomatedSystem.settings')

# Set the application to be the default ASGI application for HTTP requests
application = get_asgi_application()
