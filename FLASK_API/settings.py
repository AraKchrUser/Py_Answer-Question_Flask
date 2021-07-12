import os
import argparse


def main():

    print('Рабочий каталог', os.getcwd(), sep=' ')
    parse = argparse.ArgumentParser()
    parse.add_argument('--file', type=str, help='Файл, где должны быть сохранены почта и пароль пользователя')
    parse.add_argument('--email', type=str)
    parse.add_argument('--password', type=str)
    args = parse.parse_args()

    if not os.path.isdir('/'.join(args.file.split('/')[:-1])):
        print('Директория не существует')
        return

    if os.access(args.file, os.F_OK):
        print('Файл существует и будет перезаписан, Вы уверены? y/n')
        if input() == 'n':
            return

        if not os.access(args.file, os.W_OK):
            print('Файл не доступен для записи')
            return

    #  Создает или перезаписывает файл
    with open(args.file, 'w') as file:
        file.write(args.email + '\n' + args.password)


if __name__ == '__main__':
    main()
