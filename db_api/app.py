import os
import uvicorn
from src.config import engine
from src.models import Base

DB_API_HOST = os.getenv("DB_API_HOST", "db_api")
DB_API_PORT = int(os.getenv("DB_API_PORT", "3000"))

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    uvicorn.run(
        "src.main:app",
        reload=True,
        host=DB_API_HOST,
        port=DB_API_PORT,
    )
