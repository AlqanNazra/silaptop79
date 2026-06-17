import os
import django

import sys
import os
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "silaptop79.settings")
django.setup()

from django.test import Client
client = Client()
try:
    print("Sending GET request to /hc/manajemen-user/...")
    response = client.get('/hc/manajemen-user/')
    print("Response Status Code:", response.status_code)
except Exception as e:
    import traceback
    traceback.print_exc()
