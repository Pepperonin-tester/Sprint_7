import allure
import requests
from urls import COURIER_URL

class TestCreateCourier:
    def test_create_courier_success(self, courier):
        with allure.step("Отправить запрос на создание курьера"):
            payload, response = courier

        with allure.step("Проверить код ответа 201"):
            assert response.status_code == 201

        with allure.step("Проверить тело ответа {'ok': true}"):
            assert response.json()["ok"] == True

    def test_create_courier_with_same_login(self, courier):
        with allure.step("Отправить повторный запрос с тем же логином"):
            payload, _ = courier
            response = requests.post(COURIER_URL, json=payload)

        with allure.step("Проверить код ответа 409"):
            assert response.status_code == 409

        with allure.step("Проверить сообщение об ошибке"):
            assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."

    def test_create_courier_without_login(self):
        with allure.step("Отправить запрос без поля login"):
            payload = {"password": "152235", "firstName": "Test"}
            response = requests.post(COURIER_URL, json=payload)

        with allure.step("Проверить код ответа 400"):
            assert response.status_code == 400

        with allure.step("Проверить сообщение об ошибке"):
            assert response.json()["message"] == "Недостаточно данных для создания учетной записи"