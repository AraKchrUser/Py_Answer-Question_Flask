import argparse


def terminal_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--first_run', action='store_true', help='Запускается ли программа в первый раз')
    parser.add_argument('--email', type=str, required=False, help='Email при авторизации')
    parser.add_argument('--password', type=str, required=False, help='Пароль при авторизации')
    parser.add_argument('--register', action='store_true', help='Регистрация в базе данных')
    parser.add_argument('--config', required=False, type=argparse.FileType('r'), help='Файл, где хранятся '
                                                                                      'emil и password')
    args = parser.parse_args()

    args_list = dict()
    args_list['first_run'] = args.first_run
    args_list['email'] = args.email
    args_list['password'] = args.password
    args_list['register'] = args.register
    if args.config:
        args_list['config'] = args.config.read().split('\n')
    else:
        args_list['config'] = None

    return args_list


if __name__ == "__main__":
    print(terminal_arguments())
