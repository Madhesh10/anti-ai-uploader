# test_import_with_settings.py
import os, importlib, traceback

# 1) point to your settings module (project package name)
os.environ['DJANGO_SETTINGS_MODULE'] = 'anti_ai_uploader.settings'

# 2) now setup Django so apps & models are ready
import django
django.setup()

print('DJANGO_SETTINGS_MODULE ->', os.environ['DJANGO_SETTINGS_MODULE'])

try:
    m = importlib.import_module('uploader.views')
    print('SUCCESS: imported', m)
except Exception:
    print('ERROR during import:')
    traceback.print_exc()
