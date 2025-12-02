import os, importlib, traceback
os.environ['DJANGO_SETTINGS_MODULE']='anti_ai_uploader.settings'
try:
    importlib.import_module('anti_ai_uploader.settings')
    print('settings OK')
except Exception:
    traceback.print_exc()
