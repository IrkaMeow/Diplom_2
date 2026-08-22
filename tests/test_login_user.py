import pytest
import requests
import allure
from config import Urls, ResponseMessages as RM

@allure.epic('Авторизация пользователя')
class TestLoginUser:
    @allure.title('Успешная авторизация пользователя')
    def test_login_user_success(self, create_new_user):
        payload = create_new_user.copy()

        del payload['name']

        with allure.step('Отправляем запрос на авторизацию пользователя'):
            response = requests.post(Urls.LOGIN_USER, json=payload)

        assert response.status_code == 200
        assert response.json()['success'] == True
        assert 'accessToken' in response.json() 

    @pytest.mark.parametrize('incorrect_field', [
        {'email' : 'WrongEmail'},
        {'password' : 'WrongPassword'},
        {'email' : 'WrongEmail', 'password' : 'WrongPassword'}
    ])
    @allure.title('Вход с неверным логином/паролем')
    def test_login_user_with_incorrect_password_email_error(self, incorrect_field, create_new_user):
        payload = create_new_user.copy()
        del payload['name']

        payload.update(incorrect_field)

        with allure.step('Отправляем запрос на авторизацию с неверными данными'):
            response = requests.post(Urls.LOGIN_USER, json=payload)

        assert response.status_code == 401
        assert response.json()['message'] == RM.LOGIN_INCORRECT_FIELD
