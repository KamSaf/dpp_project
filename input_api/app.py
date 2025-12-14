import os
import uvicorn

host = os.getenv("CONTAINER_API_HOST")
port = os.getenv("CONTAINER_API_PORT")

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        reload=True,
        host=host if host else "0.0.0.0",
        port=int(port) if port else 8000,
    )
