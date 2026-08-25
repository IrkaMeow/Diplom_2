import pytest
import allure
import generators as G
from config import ResponseMessages as RM

@allure.epic('Регистрация пользователя')
class TestRegisterUser:
    @allure.title('Успешная регистрация пользователя')
    def test_create_user_success(self, api, user_data_generation):
        payload = user_data_generation

        response = api.create_user(payload)

        assert response.status_code == 200
        assert response.json()['success'] == True


    @allure.title('Попытка создать уже существующего пользователя')
    def test_create_double_user_error(self, api, create_new_user):
        payload = create_new_user

        response = api.create_user(payload)

        assert response.status_code == 403
        assert response.json()['message'] == RM.CREATE_DOUBLE_LOGIN

    @pytest.mark.parametrize('payload', [
        # не передаем name
        {'email' : G.email_generator(), 'password' : G.password_generator()}, 
        # не передаем password
        {'email' : G.email_generator(), 'name' : G.name_generator()},
        # не передаем email
        {'password' : G.password_generator(), 'name' : G.name_generator()}
    ])
    @allure.title('Попытка создать пользователя, не заполнив обязательное поле')
    def test_create_user_without_email_password_name_error(self, api, payload):

        response = api.create_user(payload)

        assert response.status_code == 403
        assert response.json()['message'] == RM.CREATE_MISSING_FIELD
