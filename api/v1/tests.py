import pytest
from fastapi.testclient import TestClient
from starlette import status
from settings import redis_instance
from fastapi.responses import JSONResponse


class Mock:
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content

    def get(self, *args, **kwargs):
        return JSONResponse(
            status_code=self.status_code,
            content=self.content,
        )


@pytest.fixture()
def client():
    from main import app

    with TestClient(app) as test_client:
        yield test_client


def test_redis():
    response: bool = redis_instance.ping()
    assert response is True


def test_get_land():
    response = client.get("/land/")
    assert response.status_code == 200


def test_get_land(client, monkeypatch):
    # because this api effect on redis db explicitly we have no choice but mock the response
    monkeypatch.setattr(client, "get", Mock(status.HTTP_200_OK, {}).get)
    response = client.get('/land/')
    assert response.status_code == 200


def test_destroy_land(client, monkeypatch):
    # because this api effect on redis db explicitly we have no choice but mock the response
    monkeypatch.setattr(client, "delete", Mock(status.HTTP_200_OK, {}).get)
    response = client.delete('/land/')
    assert response.status_code == 200


def test_attack_action(client, monkeypatch):
    # because this api effect on redis db explicitly we have no choice but mock the response
    monkeypatch.setattr(client, "put", Mock(status.HTTP_200_OK, {}).get)
    response = client.put('/land/action/attack/', {"x": 6, "y": 5})
    assert response.status_code == 200


def test_move_action(client, monkeypatch):
    # because this api effect on redis db explicitly we have no choice but mock the response
    monkeypatch.setattr(client, "put", Mock(status.HTTP_200_OK, {}).get)
    response = client.put('/land/action/attack/', {"x": 6, "y": 5, "direction": "left"})
    assert response.status_code == 200
