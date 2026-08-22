class Urls:
    BASE_URL = "https://stellarburgers.education-services.ru/"
    
    # Ссылки для запросов по пользователям 
    REGISTR_USER = f"{BASE_URL}api/auth/register"
    LOGIN_USER = f"{BASE_URL}api/auth/login"
    DATA_USER = f"{BASE_URL}api/auth/user"
    
    # Ссылки для запросов по ингредиентам и заказам
    INGREDIENTS = f"{BASE_URL}api/ingredients"
    ORDERS = f"{BASE_URL}api/orders"

class ResponseMessages:
    MISSING_INGREDIENT = 'Ingredient ids must be provided'
    CREATE_DOUBLE_LOGIN = 'User already exists'
    CREATE_MISSING_FIELD = 'Email, password and name are required fields'
    LOGIN_INCORRECT_FIELD = 'email or password are incorrect'
    ORDER_WITHOUT_LOGIN = 'You should be authorised'