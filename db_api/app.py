import os
import uvicorn
from src.config import engine
from src.models import Base

host = os.getenv("CONTAINER_API_HOST", "localhost")
port = int(os.getenv("CONTAINER_API_PORT", "8000"))

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    uvicorn.run(
        "src.main:app",
        reload=True,
        host=host,
        port=port,
    )
