import requests
import allure
import pytest
from config import Urls, ResponseMessages as RM

@allure.epic('Создание заказа')
class TestCreateOrder:
    @allure.title('Создание заказа с ингредиентами авторизованным/неавторизованным пользователем')
    @pytest.mark.parametrize('headers_type', ['auth', 'unauth'])
    def test_create_order_with_ingredient_success(self, headers_type, user_login, get_ingredients):
        payload = {
            'ingredients' : get_ingredients
        }

        headers_map = {
            'auth' : {'Authorization' : user_login['accessToken']},
            'unauth' : {}
        }
        headers = headers_map[headers_type]

        with allure.step('Отправляем запрос на создание заказа'):
            response = requests.post(Urls.ORDERS, json=payload, headers = headers)

        assert response.status_code == 200
        assert response.json()['success'] == True
        assert 'number' in response.json()['order']



    @allure.title('Попытка создать заказ с некорректным хешем ингредиента авторизованным пользователем')
    def test_create_order_incorrect_id_ingredient_error(self, user_login):
        headers = {
            'Authorization' : user_login['accessToken']
        }

        with allure.step('Отправляем запрос на создание заказа с неверным хешом ингредиента'):
            response = requests.post(Urls.ORDERS, json = {'ingredients' : ['1']}, headers=headers)

        assert response.status_code == 500



    @allure.title('Попытка создать заказ БЕЗ ингредиента авторизованным пользователем')
    def test_create_order_without_ingredient_error(self, user_login):
        headers = {
            'Authorization' : user_login['accessToken']
        }

        with allure.step('Отправляем запрос на создание заказа БЕЗ ингредиентов'):
            response = requests.post(Urls.ORDERS, headers=headers)

        assert response.status_code == 400
        assert response.json()['success'] == False
        assert response.json()['message'] == RM.MISSING_INGREDIENT