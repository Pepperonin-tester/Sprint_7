import pytest
import allure
import requests
from urls import ORDERS_URL
from data import ORDER_DATA

class TestCreateOrder:
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order(self, color):
        with allure.step(f"Подготовить данные заказа с цветом {color}"):
            payload = ORDER_DATA.copy()
            payload["color"] = color

        with allure.step("Отправить запрос на создание заказа"):
            response = requests.post(ORDERS_URL, json=payload)

        with allure.step("Проверить код ответа 201"):
            assert response.status_code == 201

        with allure.step("Проверить что ответ содержит track"):
            assert "track" in response.json()
