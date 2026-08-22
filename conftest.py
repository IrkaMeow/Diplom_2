import pytest
import requests
import allure
import generators
from config import Urls

# генерирует случайные данные пользователя
@pytest.fixture
def user_data_generation():
    return {
        'email': generators.email_generator(),
        'password': generators.password_generator(),
        'name': generators.name_generator()
    }

# регистрирует и удаляет пользователя
@pytest.fixture
def create_new_user(user_data_generation):
    payload = user_data_generation

    with allure.step('Отправляем запрос на регистрацию пользователя'):
        response = requests.post(Urls.REGISTR_USER, json=payload)

    if response.status_code != 200:
        raise RuntimeError(f'Регистрация не удалась. Код: {response.status_code}, ответ: {response.text}')

    accessToken = response.json()['accessToken']

    yield {
        'email': payload['email'],
        'password': payload['password'],
        'name' : payload['name']
    }

    with allure.step('Отправляем запрос на удаление пользователя'):
        requests.delete(Urls.DATA_USER, headers={'Authorization': accessToken})


# авторизация пользователя
@pytest.fixture
def user_login(create_new_user):
    user_data = create_new_user

    payload = {
        'email': user_data['email'],
        'password': user_data['password'],
    }

    with allure.step('Отправляем запрос на авторизацию пользователя'):
        response = requests.post(Urls.LOGIN_USER, json=payload)
        accessToken = response.json()['accessToken']
    yield {
        'email': payload['email'],
        'password': payload['password'],
        'accessToken' : accessToken
    }

# собирает 5 первых хешей ингредиентов
@pytest.fixture(scope='module')
def get_ingredients():
    with allure.step('Отправляем запрос на доступные ингредиенты'):
        response = requests.get(Urls.INGREDIENTS)

    if response.status_code != 200:
        raise RuntimeError(f'Не удалось получить ингредиенты. Код ошибки: {response.status_code}')

    return [ingredient['_id'] for ingredient in response.json()['data']][:5]