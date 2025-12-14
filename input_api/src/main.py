from fastapi import FastAPI, Body, Response
from src.services import create_task

app = FastAPI()


@app.post("/enqueue", status_code=201)
def enqueue_task(response: Response, data: dict = Body(...)) -> dict:
    try:
        create_task(data["img_url"])
        return {"message": "New task created."}
    except Exception:
        response.status_code = 500
        return {"message": "Unexpected error occured."}
