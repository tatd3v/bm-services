import uvicorn
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "app")))

if __name__ == "__main__":
    try:
        if os.geteuid() == 0:
            uvicorn.run("app.main:app", host="0.0.0.0", port=80, reload=True)
        else:
            print("Running without elevated privileges. Defaulting to port 8000.")
            uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    except AttributeError:
        print("Elevated privilege check is not supported on this platform.")
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
