import pytest
import allure
import requests
from urls import ORDERS_URL

class TestGetOrders:
    @allure.title("Получение списка заказов")
    def test_get_orders(self):
        with allure.step("Отправить запрос на получение списка заказов"):
            response = requests.get(ORDERS_URL)
        with allure.step("Проверить код ответа 200"):
            assert response.status_code == 200
        with allure.step("Проверить что ответ содержит список заказов"):
            assert "orders" in response.json()
