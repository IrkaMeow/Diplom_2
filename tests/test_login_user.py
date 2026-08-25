import pytest
import allure
from config import ResponseMessages as RM

@allure.epic('Авторизация пользователя')
class TestLoginUser:
    @allure.title('Успешная авторизация пользователя')
    def test_login_user_success(self, api, create_new_user):
        payload = create_new_user.copy()
        del payload['name']

        response = api.authorize_user(payload)

        assert response.status_code == 200
        assert response.json()['success'] == True
        assert 'accessToken' in response.json() 

    @pytest.mark.parametrize('incorrect_field', [
        {'email' : 'WrongEmail'},
        {'password' : 'WrongPassword'},
        {'email' : 'WrongEmail', 'password' : 'WrongPassword'}
    ])
    @allure.title('Вход с неверным логином/паролем')
    def test_login_user_with_incorrect_password_email_error(self, api, incorrect_field, create_new_user):
        payload = create_new_user.copy()
        del payload['name']
        payload.update(incorrect_field)

        response = api.authorize_user(payload)

        assert response.status_code == 401
        assert response.json()['message'] == RM.LOGIN_INCORRECT_FIELD
