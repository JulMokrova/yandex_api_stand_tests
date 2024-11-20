import data

import sender_stand_request
from data import user_body
from sender_stand_request import response


def get_user_body(first_name):
    # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_body = data.user_body.copy()
    # изменение значения в поле firstName
    current_body["firstName"] = first_name
    # возвращается новый словарь с нужным значением firstName
    return current_body

def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    # Проверяется, что код ответа равен 201
    assert user_response.status_code == 201
    # Проверяется, что в ответе есть поле authToken и оно не пустое
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()
    # Конструирование строки str_user с данными пользователя и токеном авторизации.
    # Сначала добавляется имя пользователя из словаря user_body.
    # Затем через запятую добавляется номер телефона пользователя из того же словаря.
    # После этого добавляется адрес пользователя, также из словаря user_body.
    # Далее следуют три запятые, разделяющие данные пользователя от токена авторизации.
    # В конце добавляется токен авторизации, извлеченный из JSON-ответа сервера после выполнения запроса к API.
    # Использование обратной косой черты (\) в конце первой строки позволяет перенести часть кода на новую строку для лучшей читаемости.
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    assert users_table_response.text.count(str_user) == 1
# Тест 1. Успешное создание пользователя
# Параметр firstName состоит из 2 символов
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")

def negative_assert_symbol(first_name):
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body(first_name)
    # В переменную response сохраняется результат запроса
    response = sender_stand_request.post_new_user(user_body)
    #Проверяет, чтокод  ответа 400
    assert response.status_code == 400
    #Проверяет, что в теле ответа атрибут code — 400
    assert response.json()["code"] == 400
    #Проверяет, что в теле ответа атрибут message такой:"Имя пользователя введено некорректно. Имя может содержать только русские или латинские буквы, длина должна быть не менее 2 и не более 15 символов"
    assert response.json()["message"] == "Имя пользователя введено некорректно. Имя может содержать только русские или латинские буквы, длина должна быть не менее 2 и не более 15 символов"

# Тест 3. Ошибка
    # Параметр fisrtName состоит из 1 символа
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("А")

# Тест 4. Ошибка
    # Параметр fisrtName состоит из 16 символов
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Аааааааааааааааа")

# Тест 5.Успешное создание пользователя 
    # Параметр fisrtName состоит из лат символов
def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("Abcd")

# Тест 6.Успешное создание пользователя
    # Параметр fisrtName состоит из рус символов
def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert("Русскиебуквы")

# Тест 7.Ошибка при пробелах
    # Параметр fisrtName содержит пробелы
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("Человек и Ко")

# Тест 8.Ошибка
    # Параметр fisrtName содержит спецсимволы
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("№%@")

# Тест 9.Ошибка
    # Параметр fisrtName содержит цифры
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")

# Функция для негативной проверки
    # В ответе ошибка: "Не все необходимые параметры были переданы"
def negative_assert_no_first_name(user_body):
    # В переменную response сохраняется результат запроса
    response = sender_stand_request.post_new_user(user_body)
    # Проверяет, чтокод  ответа 400
    assert response.status_code == 400
    # Проверяет, что в теле ответа атрибут code — 400
    assert response.json()["code"] == 400
    # Проверяет, что в теле ответа атрибут message такой:"Не все необходимые параметры были переданы"
    assert response.json()["message"] == "Не все необходимые параметры были переданы"

# Тест 10. Ошибка
# В запросе нет параметра firstName
def test_create_user_no_first_name_get_error_response():
    # Копируется словарь с телом запроса из файла data в переменную user_body
    # Иначе можно потерять данные из исходного словаря
    user_body = data.user_body.copy()
    # Удаление параметра firstName из запроса
    user_body.pop("firstName")
    # Проверка полученного ответа
    negative_assert_no_first_name(user_body)

# Тест 11. Ошибка
# Параметр fisrtName состоит из пустой строки
def test_create_user_empty_first_name_get_error_response():
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body("")
    # Проверка полученного ответа
    negative_assert_no_first_name(user_body)

# Тест 12. Ошибка
# Параметр fisrtName  - другой тип данных
def test_create_user_number_type_first_name_get_error_response():
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body=get_user_body(12)
    # В переменную user_response сохраняется результат запроса на создание пользователя:
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400