import allure
import random
import string
import requests
from urls import COURIER_URL, COURIER_LOGIN_URL
from data import COURIER_ALREADY_EXISTS, COURIER_NOT_ENOUGH_DATA

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

class TestCreateCourier:
    def test_create_courier_success(self):
        with allure.step("Подготовить данные нового курьера"):
            payload = {
                "login": generate_random_string(8),
                "password": generate_random_string(6),
                "firstName": generate_random_string(10)
            }

        with allure.step("Отправить запрос на создание курьера"):
            response = requests.post(COURIER_URL, json=payload)

        with allure.step("Проверить код ответа 201"):
            assert response.status_code == 201

        with allure.step("Проверить тело ответа {'ok': true}"):
            assert response.json()["ok"] == True

        with allure.step("Удалить созданного курьера"):
            courier_id = requests.post(COURIER_LOGIN_URL, json=payload).json()["id"]
            requests.delete(f"{COURIER_URL}/{courier_id}")

    def test_create_courier_with_same_login(self, courier):
        with allure.step("Отправить повторный запрос с тем же логином"):
            payload, _ = courier
            response = requests.post(COURIER_URL, json=payload)

        with allure.step("Проверить код ответа 409"):
            assert response.status_code == 409

        with allure.step("Проверить сообщение об ошибке"):
            assert response.json()["message"] == COURIER_ALREADY_EXISTS

    def test_create_courier_without_login(self):
        with allure.step("Отправить запрос без поля login"):
            payload = {"password": "152235", "firstName": "Test"}
            response = requests.post(COURIER_URL, json=payload)

        with allure.step("Проверить код ответа 400"):
            assert response.status_code == 400

        with allure.step("Проверить сообщение об ошибке"):
            assert response.json()["message"] == COURIER_NOT_ENOUGH_DATA
    
    def test_create_courier_without_password(self):
        with allure.step("Отправить запрос без поля password"):
            payload = {"login": "testlogin531", "firstName": "Test"}
            response = requests.post(COURIER_URL, json=payload)

        with allure.step("Проверить код ответа 400"):
            assert response.status_code == 400

        with allure.step("Проверить сообщение об ошибке"):
            assert response.json()["message"] == COURIER_NOT_ENOUGH_DATA

    def test_create_courier_without_first_name(self):
        with allure.step("Подготовить данные нового курьера"):
            payload = {
                "login": generate_random_string(8),
                "password": generate_random_string(6)
            }

        with allure.step("Отправить запрос на создание курьера"):
            response = requests.post(COURIER_URL, json=payload)

        with allure.step("Проверить код ответа 201"):
            assert response.status_code == 201

        with allure.step("Проверить тело ответа {'ok': true}"):
            assert response.json()["ok"] == True

        with allure.step("Удалить созданного курьера"):
            courier_id = requests.post(COURIER_LOGIN_URL, json=payload).json()["id"]
            requests.delete(f"{COURIER_URL}/{courier_id}")
