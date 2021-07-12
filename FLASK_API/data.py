class Data:
    """Хранит значения полей 'текст', 'вопрос', 'ответ' формы"""

    def __init__(self):
        self.text = ''
        self.question = ''
        self.answer = ''

    def set_text(self, text):
        self.text = text

    def set_answer(self, answer):
        self.answer = answer

    def set_question(self, question):
        self.question = question

    def get_text(self):
        return self.text

    def get_answer(self):
        return self.answer

    def get_question(self):
        return self.question
