"""Клиентское приложение асинхронного чата"""
import argparse
import sys
import os
import configparser
from PyQt5.QtWidgets import QApplication
from Cryptodome.PublicKey import RSA

from common.constants import *
from common.errors import ServerError
from common.decos import log
from database import ClientDatabase
from transport import ClientTransport
from main_window import ClientMainWindow
from start_dialog import UserNameDialog

# Инициализация клиентского логера
logger = logging.getLogger('client_src')


@log
def arg_parser():
    """Парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        logger.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    return server_address, server_port, client_name


def config_load(name: str):
    """загрузчик конфигурации из .ini файла"""
    config = configparser.ConfigParser()
    config_path = f"{f'client_{name}.ini'}"
    config.read(config_path)
    # Если конфиг файл загружен правильно, запускаемся, иначе конфиг по умолчанию.
    if 'SETTINGS' in config:
        return config
    else:
        config.add_section('SETTINGS')
        config.set('SETTINGS', 'theme', '1')
        with open(config_path, 'w') as config_file:
            config.write(config_file, config)
        return config


def get_rsa_keys(name):
    """get RSA key. Create if not exist."""
    dir_path = os.getcwd()
    key_path = os.path.join(dir_path, f'{name}.key')
    if not os.path.exists(key_path):
        keys = RSA.generate(2048, os.urandom)
        with open(key_path, 'wb') as key_file:
            key_file.write(keys.export_key())
    else:
        with open(key_path, 'rb') as key_file:
            keys = RSA.import_key(key_file.read())
    return keys


# Основная функция клиента
if __name__ == '__main__':
    # Загружаем параметы коммандной строки
    server_address, server_port, client_name = arg_parser()

    # Создаём клиентокое приложение
    client_app = QApplication(sys.argv)

    # Если имя пользователя не было указано в командной строке то запросим его
    if not client_name:
        start_dialog = UserNameDialog()
        client_app.exec_()
        # Если пользователь ввёл имя и нажал ОК, то сохраняем ведённое и удаляем объект, инааче выходим
        if start_dialog.ok_pressed:
            client_name = start_dialog.client_name.text()
            client_password = start_dialog.client_password.text()
            del start_dialog
        else:
            sys.exit(0)

    # Записываем логи
    logger.info(f'Запущен клиент с парамертами: адрес сервера: {server_address}, '
                f'порт: {server_port}, имя пользователя: {client_name}')

    rsa_keys = get_rsa_keys(client_name)
    # Создаём объект базы данных
    database = ClientDatabase(client_name)

    # Создаём объект - транспорт и запускаем транспортный поток
    try:
        transport = ClientTransport(server_port, server_address, database, client_name, client_password, rsa_keys)
    except ServerError as error:
        print(error.text)
        sys.exit(1)
    transport.setDaemon(True)
    transport.start()

    # читаем конфиги
    config = config_load(client_name)

    # Создаём GUI
    main_window = ClientMainWindow(database, transport)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'Чат Программа alpha release - {client_name}')
    main_window.set_theme(config)
    client_app.exec_()

    # Раз графическая оболочка закрылась, закрываем транспорт
    transport.transport_shutdown()
    transport.join()
