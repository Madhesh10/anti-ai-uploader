import importlib, traceback
print("Testing import of uploader.views...")
try:
    m = importlib.import_module("uploader.views")
    print("SUCCESS:", m)
except Exception as e:
    print("ERROR:")
    traceback.print_exc()
