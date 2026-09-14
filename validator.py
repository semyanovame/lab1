import re
import hashlib
BLACKLISTED_LOGINS = {"admin", "master", "root", "superuser", "test", "guest", "null", "undefined", "user", "username", "login", "password"}
def validate_login(login):
    if not isinstance(login, str):
        return False, "Логин должен быть строкой"
    
    if "@" in login:
        # это email — сюда позже добавим валидацию
        local_part = r"[a-zA-Z0-9._-]+" 
        domain = r"[a-zA-Z0-9-]+" 
        zone = r"[a-zA-Z]+"    
        email_pattern = "^" + local_part + "@" + domain + r"\." + zone + "$"
        if not re.match(email_pattern, login):
            return False, "email должен быть в формате local-part@domain"
    elif login.startswith("+"):
        # это телефон
        if not re.match(r"^\+\d{1}-\d{3}-\d{3}-\d{4}$", login):
            return False, "телефон должен быть в формате +x-xxx-xxx-xxxx"
    else:
        # обычная строка
        if len(login) < 5:
            return False, "Логин должен быть не короче 5 символов"
        if not re.match(r"^[a-zA-Z0-9_]+$", login):
            return False, "логин может содержать только латинские буквы, цифры и знак подчёркивания"
        if login.lower() in BLACKLISTED_LOGINS:
            return False, "логин не может быть из черного списка"
    return True, ""

def validate_password(password):
    if not isinstance(password, str):
        return False, "Пароль должен быть строкой"
    
    if len(password) < 7:
        return False, "Пароль должен быть не короче 7 символов"
    if not re.match(r"^[а-яА-ЯёЁ0-9!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]+$", password):
        return False, "Пароль может содержать только русские буквы, цифры и специальные символы"
    if not re.search(r"[А-ЯЁ]", password):
        return False, "Пароль должен содержать хотя бы одну заглавную русскую букву"
    if not re.search(r"[а-яё]", password):
        return False, "Пароль должен содержать хотя бы одну строчную русскую букву"
    if not re.search(r"\d", password):
        return False, "Пароль должен содержать хотя бы одну цифру"
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
        return False, "Пароль должен содержать хотя бы один специальный символ"
    return True, ""

def password_correctness(password, confirm_password):
    if password != confirm_password:
        return False, "Пароли не совпадают"
    return True, ""

def validate_main(login, password, confirm_password):
    login_valid, login_error = validate_login(login)
    if not login_valid:
        return False, login_error
    
    password_valid, password_error = validate_password(password)
    if not password_valid:
        return False, password_error
    
    correctness_valid, correctness_error = password_correctness(password, confirm_password)
    if not correctness_valid:
        return False, correctness_error
    
    return True, ""


def hash_password(password):
    # Используем SHA-256 для хэширования пароля
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()