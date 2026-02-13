import uvicorn
import os
import sys

if __name__ == "__main__":
    # Ensure current directory is in python path
    sys.path.append(os.getcwd())
    
    print("🚀 Starting test...")
    print("📍 Local URL: http://localhost:8000")
    print("📄 Docs URL:  http://localhost:8000/api/v1/docs")
    
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)