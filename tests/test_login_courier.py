import allure
import requests
from urls import COURIER_LOGIN_URL
from data import COURIER_NOT_FOUND, COURIER_NOT_ENOUGH_DATA_LOGIN

class TestLoginCourier:
    def test_login_courier_success(self, courier):
        with allure.step("Получить данные курьера из фикстуры"):
            payload, _ = courier

        with allure.step("Отправить запрос на логин курьера"):
            response = requests.post(COURIER_LOGIN_URL, json=payload)

        with allure.step("Проверить код ответа 200"):
            assert response.status_code == 200

        with allure.step("Проверить что ответ содержит id"):
            assert "id" in response.json()

    def test_login_courier_with_wrong_password(self, courier):
        with allure.step("Получить данные курьера и подменить пароль"):
            payload, _ = courier
            wrong_payload = {"login": payload["login"], "password": "wrong_password"}

        with allure.step("Отправить запрос с неверным паролем"):
            response = requests.post(COURIER_LOGIN_URL, json=wrong_payload)

        with allure.step("Проверить код ответа 404"):
            assert response.status_code == 404

        with allure.step("Проверить сообщение об ошибке"):
            assert response.json()["message"] == COURIER_NOT_FOUND

    def test_login_courier_without_login(self):
        with allure.step("Отправить запрос без поля login"):
            payload = {"password": "152235"}
            response = requests.post(COURIER_LOGIN_URL, json=payload)

        with allure.step("Проверить код ответа 400"):
            assert response.status_code == 400

        with allure.step("Проверить сообщение об ошибке"):
            assert response.json()["message"] == COURIER_NOT_ENOUGH_DATA_LOGIN

    def test_login_courier_with_nonexistent_user(self):
        with allure.step("Отправить запрос с несуществующим пользователем"):
            payload = {"login": "21dsfs", "password": "123fz3"}
            response = requests.post(COURIER_LOGIN_URL, json=payload)

        with allure.step("Проверить код ответа 404"):
            assert response.status_code == 404

        with allure.step("Проверить сообщение об ошибке"):
            assert response.json()["message"] == COURIER_NOT_FOUND
            