import allure
import pytest
from config import ResponseMessages as RM

@allure.epic('Создание заказа')
class TestCreateOrder:
    @allure.title('Создание заказа с ингредиентами авторизованным/неавторизованным пользователем')
    @pytest.mark.parametrize('headers_type', ['auth', 'unauth'])
    def test_create_order_with_ingredient_success(self, headers_type, api, user_login, get_ingredients):
        payload = {
            'ingredients' : get_ingredients
        }

        headers_map = {
            'auth' : {'Authorization' : user_login['accessToken']},
            'unauth' : {}
        }
        headers = headers_map[headers_type]

        response = api.create_order(payload, headers)

        assert response.status_code == 200
        assert response.json()['success'] == True
        assert 'number' in response.json()['order']



    @allure.title('Попытка создать заказ с некорректным хешем ингредиента авторизованным пользователем')
    def test_create_order_incorrect_id_ingredient_error(self, api, user_login):
        headers = {
            'Authorization' : user_login['accessToken']
        }
        payload = {'ingredients':['1']}

        response = api.create_order(payload, headers)

        assert response.status_code == 500



    @allure.title('Попытка создать заказ БЕЗ ингредиента авторизованным пользователем')
    def test_create_order_without_ingredient_error(self, api, user_login):
        headers = {
            'Authorization' : user_login['accessToken']
        }

        response = api.create_order(headers=headers) 

        assert response.status_code == 400
        assert response.json()['success'] == False
        assert response.json()['message'] == RM.MISSING_INGREDIENT
        