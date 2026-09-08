import requests
import allure
from config import Urls 

class BurgerApiClient:
    @allure.step('Отправляем запрос на доступные ингредиенты')
    def access_ingredients(self):
        return requests.get(Urls.INGREDIENTS)

    @allure.step('Отправляем запрос на создание заказа')
    def create_order(self, payload=None, headers=None):
        return requests.post(Urls.ORDERS, json=payload, headers = headers)

    @allure.step('Отправляем запрос на регистрацию пользователя')
    def create_user(self, payload):
        return requests.post(Urls.REGISTR_USER, json=payload)

    @allure.step('Отправляем запрос на авторизацию пользователя')
    def authorize_user(self, payload):
        return requests.post(Urls.LOGIN_USER, json=payload)

    @allure.step('Отправляем запрос на удаление пользователя')
    def remove_user(self, accessToken):
        return requests.delete(Urls.DATA_USER, headers={'Authorization': accessToken})
    
