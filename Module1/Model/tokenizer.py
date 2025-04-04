# для чтения json файлов
import json
# для обработки текста
import re


class Tokenizer():
    # конструктор класса
    def __init__(self):
        import os
        print(os.getcwd())
        try:
            with open("Module1/Model/text_to_id.json", "r", encoding="utf-8") as f:
                self.text_to_ids_voc = json.load(f)
            
            with open("Module1/Model/id_to_text.json", "r", encoding="utf-8") as f:
                self.id_to_text_voc = {int(k): v for k, v in json.load(f).items()}
        
        except FileNotFoundError:
            print("Ошибка: JSON-файлы не найдены. Создайте их сначала.")
            raise
        except json.JSONDecodeError:
            print("Ошибка: Файлы повреждены. Удалите их и пересоздайте.")
            raise
        
    # функция для предобработки текста
    @staticmethod
    def process_text(text: str) -> str:
        '''Ф-я для обработки текста'''
        # приводим к нижнему регистру
        text = text.lower()
        # убираем лишние символы
        text = re.sub(r'[^a-z^А-я0-9\s]', '', text).strip()
        # обработка лишних пробелов
        text = re.sub(r'\s+', ' ', text).strip()
        # разбиваем текст на части сохраняя пробелы
        parts = re.split(r'(\s+)', text)

        # список для токенов
        tokens = []
        # проходимся по каждой части
        for part in parts:
            # если это пробел
            if part.isspace():
                # добавляем заменяющий токен
                tokens.append('_')
            # если не пробел
            elif part:
                # сохраняем токен
                tokens.append(part)
                
        # возврашаем токенизированный текст
        return tokens

    # обратная обработка текста
    @staticmethod
    def back_processing(tokens: list):
        # список для частей текста
        text_data = []
        for token in tokens:
            # меняем _ на пробелы
            if token == '_':
                text_data.append(' ')
            # добавляем токен
            else:
                text_data.append(token)
        # возвращаем текст
        return ''.join(text_data)

    # функция для токенизации
    def text_to_ids(self, text: str):
        return [self.text_to_ids_voc.get(token, self.text_to_ids_voc['<unk>']) for token in self.process_text(text)]

    # функция для обратной токенизации
    def id_to_text(self, ids):
        return self.back_processing(([self.id_to_text_voc.get(idx, '<unk>') for idx in ids]))