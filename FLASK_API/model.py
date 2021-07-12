# -*- coding: utf-8 -*-

from deeppavlov import build_model, configs


class Model:
    """Хранит предобученную deeppavlov-модель для ответа на вопрос"""

    def __init__(self, download=True):
        # При первом запуске download=True
        self.model_ru = build_model(configs.squad.squad_ru_rubert, download=download)

        # Начальная инициализация текста и вопроса
        self.text = ('Первая многоразовая ступень ракеты-носителя Falcon 9 успешно отделилась через две с половиной '
                     'минуты после старта и автоматически приземлилась на плавучую платформу Of Course I Still Love '
                     'You у берегов '
                     'Флориды. Через 12 минут после запуска космический корабль Crew Dragon вышел на расчетную орбиту '
                     'и отделился '
                     'от второй ступени ракеты. Сближение корабля Crew Dragon с Международной космической станцией '
                     'запланировано '
                     'на 31 мая. К стыковочному адаптеру на узловом модуле «Гармония» американского сегмента МКС Crew '
                     'Dragon '
                     'должен причалить в ручном или, при необходимости, в автоматическом режиме. Эта процедура '
                     'запланирована '
                     'на 10:29 по времени Восточного побережья США (17:29 по московскому времени).'
                     'В испытательном полете DM2 астронавт Херли является командиром космического корабля (spacecraft '
                     'commander), '
                     'а его напарник Бенкен — командир по операциям стыковки и расстыковки (joint operations '
                     'commander). Фактически '
                     'это означает, что именно Херли управляет Crew Dragon в полете к МКС, к которой они должны '
                     'пристыковаться в '
                     'течение суток после старта. Херли и Бенкен также будут выполнять необходимые для сертификации '
                     'НАСА проверки '
                     'систем корабля в полете. Во время полета Херли и Бенкен провели небольшую экскурсию по Crew '
                     'Dragon.')
        self.question = 'Когда отделилась первая ступень?'

    def set_text(self, text):
        self.text = text

    def set_question(self, question):
        self.question = question

    def get_text(self):
        return self.text

    def get_question(self):
        return self.question

    def get_answer(self):
        answer = self.model_ru([self.text], [self.question])[0][0].capitalize() + '.'
        print(answer)
        return answer
