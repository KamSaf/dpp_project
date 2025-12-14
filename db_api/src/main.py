from fastapi import FastAPI, Body, Response, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.config import get_db
from src.models import Record

app = FastAPI()


@app.post("/save", status_code=201)
def save_result(
    response: Response, data: dict = Body(...), db: Session = Depends(get_db)
) -> dict:
    try:
        db.add_all([Record(img_url=data["img_url"], ppl_num=data["ppl_num"])])
        db.commit()
        return {"message": "Data successfully saved to database."}
    except Exception:
        response.status_code = 500
        return {"message": "Error occured when trying to save data to database."}


@app.get("/records", status_code=200)
def get_movies(response: Response, db: Session = Depends(get_db)) -> dict:
    try:
        stmt = select(Record)
        records = db.scalars(stmt).all()
        return {"records": map(lambda m: m.to_dict(), records)}
    except Exception:
        response.status_code = 500
        return {"message": "Unexpected errror occured."}
