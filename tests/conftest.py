import pytest
import requests
from urls import COURIER_URL, COURIER_LOGIN_URL, ORDERS_URL
from helpers import generate_random_string

@pytest.fixture
def courier():
    payload = {
        "login": generate_random_string(8),
        "password": generate_random_string(6),
        "firstName": generate_random_string(10)
    }

    response = requests.post(COURIER_URL, json=payload)
    yield payload, response

    courier_id = requests.post(COURIER_LOGIN_URL, json=payload).json()["id"]
    requests.delete(f"{COURIER_URL}/{courier_id}")

@pytest.fixture
def courier_id():
    payload = {
        "login": generate_random_string(8),
        "password": generate_random_string(6),
        "firstName": generate_random_string(10)
    }

    requests.post(COURIER_URL, json=payload)

    response = requests.post(COURIER_LOGIN_URL, json=payload)
    courier_id = response.json() ["id"]
    yield courier_id

    requests.delete(f"{COURIER_URL}/{courier_id}")

@pytest.fixture
def delete_courier():
    payloads = []
    yield payloads
    for payload in payloads:
        courier_id = requests.post(COURIER_LOGIN_URL, json=payload).json()["id"]
        requests.delete(f"{COURIER_URL}/{courier_id}")
