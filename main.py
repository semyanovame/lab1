import os
from validator import validate_main, hash_password
import sys
import logging
def main():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    # Шаблон строки лога (аналог template в Serilog)
    # Содержит: время, уровень (до 7 символов для выравнивания), имя логгера и сообщение
    log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Базовая настройка корневого логгера
    logging.basicConfig(
        level=logging.DEBUG, # Минимальный уровень логирования (аналог MinimumLevel.Debug)
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),          # Настройка логирования в консоль
            logging.FileHandler("logs/file_txt.log", encoding="utf-8") # Настройка логирования в файл
        ]
    )
    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")
    login = input("Введите логин: ")
    password = input("Введите пароль: ")
    confirm_password = input("Подтвердите пароль: ")

    is_valid, message = validate_main(login, password, confirm_password)

    if is_valid:
        logging.info(f"Валидация прошла успешно {login} {hash_password(password)} {hash_password(confirm_password)}")
    else:
        logging.error(f"{message} ({login} {hash_password(password)} {hash_password(confirm_password)})")
if __name__ == "__main__":
    main()