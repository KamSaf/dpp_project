import pytest
from sqlalchemy import select
from src.models import Record
from src.test.config import TestingSessionLocal, client


@pytest.fixture(scope="module")
def session():
    db = TestingSessionLocal()
    yield db
    db.close()


def test_save_record(session):
    payload = {"img_url": "test_image_url", "ppl_num": 4432}
    response = client.post("/save", json=payload)
    assert response.status_code == 201
    stmt = select(Record)
    records = session.scalars(stmt).all()
    assert len(records) == 1
    assert records[0].id == 1
    assert records[0].img_url == payload["img_url"]
    assert records[0].ppl_num == payload["ppl_num"]


def test_get_records(session):
    response = client.get("/records")
    assert response.status_code == 200
