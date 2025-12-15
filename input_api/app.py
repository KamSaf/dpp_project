import os
import uvicorn

INPUT_API_HOST = os.getenv("INPUT_API_HOST", "input_api")
INPUT_API_PORT = int(os.getenv("INPUT_API_PORT", "4000"))

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        reload=True,
        host=INPUT_API_HOST,
        port=INPUT_API_PORT,
    )
