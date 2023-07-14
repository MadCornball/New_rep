import openai
import json
import os
import pyperclip

# Установите ваш API-ключ ChatGPT
openai.api_key = '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'

# Путь к директории с файлами
dir_path = '/Users/vladglusko/PycharmProjects/pythonProject6/'

# Получаем список файлов в директории
files = os.listdir(dir_path)

# Счетчик запросов
request_count = 0

# Максимальное количество запросов
MAX_REQUESTS = 100

# Ищем файлы с расширением .py и копируем их содержимое в буфер обмена и отправляем в ChatGPT
for f in files:
    # Проверяем, достигнуто ли максимальное количество запросов
    if request_count >= MAX_REQUESTS:
        break

    # Путь к файлу
    file_path = os.path.join(dir_path, f)

    # Проверяем, является ли файл .py
    if os.path.isfile(file_path) and f.endswith('.py'):
        # Копируем содержимое файла в буфер обмена
        with open(file_path, 'r') as file:
            file_content = file.read()

        # Отправляем содержимое файла в ChatGPT с промптом
        prompt = """Please provide a detailed documentation of the following Python code, including comments, docstrings, 
        and type hinting. List of RULES for you: 1 The comments and docstrings should be in Russian. 2 Add comments 
        with code descriptions per raw or per code block of logic (on your opinion as what will be better). 3 You MUST 
        add similar comments and docstrings everywhere it can be and personally fill them. 3 Don't 
        skip any lines of code! 4 Don't forget about additional description comments inside code (# [
        description]). 5 Add type hinting everywhere. 6 Don't collapse parts of code for the sake of saving 
        characters. You must write the entire resulting code to replace it once instead of unreformatted code from my 
        request! 7 You can and may optimize and clean up the resulting code as much as you can. 8 Save each result in your 
        context for the learning project and its architecture for better responses in future answers. This is the 
        selected code: \n```python\n""" + file_content + "\n```\n\n---"

        # Add a template for the desired response format
        response_template = """### Documentation for the Python code:\n\n{code_doc}\n\n### Reconstructed code:\n\n```python\n{code}\n```\n\n---"""

        try:
            messages = [
                {"role": "system", "content": "You are a helpful assistant that provides code documentation."},
                {"role": "user", "content": prompt},
            ]

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
                n=1,
                stop=None,
                timeout=10,
            )

            # Увеличиваем счетчик запросов
            request_count += 1

            # Получаем ответ из ChatGPT
            response_message = response.choices[0].message
            response_text = response_message['content']

            # Проверяем наличие разделителя "---" в ответе
            if '---' in response_text:
                # Парсим ответ, чтобы получить документацию и код
                code_doc, code = response_text.split("---")

                # Заменяем шаблонные значения в шаблоне ответа
                formatted_response = response_template.format(code_doc=code_doc, code=code)

                # Копируем ответ из ChatGPT в буфер обмена
                pyperclip.copy(formatted_response)

                # Выводим результат на экран
                print(f"Содержимое файла {f}:")
                print(pyperclip.paste())
            else:
                # Выводим сообщение об ошибке
                print("Ошибка: Не удалось разделить ответ на документацию и код.")
                print("Ответ от ChatGPT:")
                print(response_text)

        except openai.error.APIError as e:
            # Обработка ошибки API
            print(f"Ошибка API: {e}")
        except Exception as e:
            # Обработка других ошибок
            print(f"Ошибка: {e}")

# Выводим количество сделанных запросов
print(f"Количество запросов: {request_count}")
