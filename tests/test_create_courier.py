import allure
import requests
from urls import COURIER_URL, COURIER_LOGIN_URL
from data import COURIER_ALREADY_EXISTS, COURIER_NOT_ENOUGH_DATA
from helpers import generate_random_string

class TestCreateCourier:
    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, delete_courier):
        with allure.step("Подготовить данные нового курьера"):
            payload = {
                "login": generate_random_string(8),
                "password": generate_random_string(6),
                "firstName": generate_random_string(10)
            }

        with allure.step("Отправить запрос на создание курьера"):
            response = requests.post(COURIER_URL, json=payload)
            delete_courier.append(payload)

        with allure.step("Проверить код ответа 201"):
            assert response.status_code == 201

        with allure.step("Проверить тело ответа {'ok': true}"):
            assert response.json()["ok"] == True

    @allure.title("Нельзя создать двух курьеров с одинаковым логином")
    def test_create_courier_with_same_login(self, courier):
        with allure.step("Получить данные существующего курьера"):
            payload, _ = courier

        with allure.step("Отправить повторный запрос с тем же логином"):
            response = requests.post(COURIER_URL, json=payload)

        with allure.step("Проверить код ответа 409"):
            assert response.status_code == 409

        with allure.step("Проверить сообщение об ошибке"):
            assert response.json()["message"] == COURIER_ALREADY_EXISTS

    @allure.title("Нельзя создать курьера без логина")
    def test_create_courier_without_login(self):
        with allure.step("Отправить запрос без поля login"):
            payload = {"password": "152235", "firstName": "Test"}
            response = requests.post(COURIER_URL, json=payload)

        with allure.step("Проверить код ответа 400"):
            assert response.status_code == 400

        with allure.step("Проверить сообщение об ошибке"):
            assert response.json()["message"] == COURIER_NOT_ENOUGH_DATA

    @allure.title("Нельзя создать курьера без пароля")
    def test_create_courier_without_password(self):
        with allure.step("Отправить запрос без поля password"):
            payload = {"login": "testlogin531", "firstName": "Test"}
            response = requests.post(COURIER_URL, json=payload)

        with allure.step("Проверить код ответа 400"):
            assert response.status_code == 400

        with allure.step("Проверить сообщение об ошибке"):
            assert response.json()["message"] == COURIER_NOT_ENOUGH_DATA

    @allure.title("Создание курьера без имени")
    def test_create_courier_without_first_name(self, delete_courier):
        with allure.step("Подготовить данные нового курьера"):
            payload = {
                "login": generate_random_string(8),
                "password": generate_random_string(6)
                }

        with allure.step("Отправить запрос на создание курьера"):
            response = requests.post(COURIER_URL, json=payload)
            delete_courier.append(payload)

        with allure.step("Проверить код ответа 201"):
            assert response.status_code == 201

        with allure.step("Проверить тело ответа {'ok': true}"):
            assert response.json()["ok"] == True
