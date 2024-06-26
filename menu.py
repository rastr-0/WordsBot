from aiogram import types


class Menu:
    @staticmethod
    def generate_keyboard(buttons):
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=buttons,
            resize_keyboard=True,
            one_time_keyboard=True
        )
        return keyboard

    @staticmethod
    def main_actions():
        kb = [
            [types.KeyboardButton(text="Мои модули\U0001F5C3")],
            [types.KeyboardButton(text="Создать модуль\U0001F6E0")],
            [types.KeyboardButton(text="Заметки\U0001F4DD")]
        ]
        return Menu.generate_keyboard(kb)

    @staticmethod
    def module_actions():
        kb = [
            [types.KeyboardButton(text="Карточки")],
            [types.KeyboardButton(text="Мультивыбор")],
            [types.KeyboardButton(text="Ассоциативное соединение слов")],
            [types.KeyboardButton(text="Письменный перевод")]
        ]
        return Menu.generate_keyboard(kb)

    @staticmethod
    def add_words():
        kb = [
            [types.KeyboardButton(text="Слова из Google Docs\U0001F310")],
            [types.KeyboardButton(text=".Слова из .txt или .xlsx файла\U0001F4C4")],
            [types.KeyboardButton(text="Вручную\U0000270D")],
            [types.KeyboardButton(text="Добавить слова позже\U000023F3")]
        ]
        return Menu.generate_keyboard(kb)

    @staticmethod
    def get_file():
        kb = [
            [types.KeyboardButton(text=".txt файл")],
            [types.KeyboardButton(text=".xlsx файл")]
        ]
        return Menu.generate_keyboard(kb)
