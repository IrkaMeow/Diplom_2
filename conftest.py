import pytest
import generators
from api_client import BurgerApiClient

# создает объект класса BurgerApiClient
@pytest.fixture
def api():
    return BurgerApiClient()

# генерирует случайные данные пользователя и удаляет его
@pytest.fixture
def user_data_generation(api):
    payload = {
        'email': generators.email_generator(),
        'password': generators.password_generator(),
        'name': generators.name_generator()
    }

    yield payload

    del payload['name']
    response = api.authorize_user(payload)
    token = response.json().get('accessToken')
    if token:
        api.remove_user(token)


# регистрирует пользователя
@pytest.fixture
def create_new_user(api, user_data_generation):
    payload = user_data_generation
    response = api.create_user(payload)

    if response.status_code != 200:
        pytest.fail(f'Регистрация пользователя не удалась. Код: {response.status_code}, ответ: {response.text}')

    yield {
        'email': payload['email'],
        'password': payload['password'],
        'name' : payload['name']
    }


# авторизация пользователя
@pytest.fixture
def user_login(api, create_new_user):
    user_data = create_new_user

    payload = {
        'email': user_data['email'],
        'password': user_data['password'],
    }

    response = api.authorize_user(payload)
    accessToken = response.json()['accessToken']
    yield {
        'email': payload['email'],
        'password': payload['password'],
        'accessToken' : accessToken
    }


# собирает 5 первых хешей ингредиентов
@pytest.fixture
def get_ingredients(api):
    response = api.access_ingredients()

    if response.status_code != 200:
        pytest.fail(f'Не удалось получить ингредиенты в фикстуре. Код ошибки: {response.status_code}')

    return [ingredient['_id'] for ingredient in response.json()['data']][:5]
