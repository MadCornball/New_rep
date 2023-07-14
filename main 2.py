import openai
import os
import pyperclip

# Установите ваш API-ключ ChatGPT
openai.api_key = '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'

# Путь к директории с файлами
dir_path = '/Users/vladglusko/PycharmProjects/pythonProject6/'

# Счетчик запросов
request_count = 0

# Максимальное количество запросов
MAX_REQUESTS = 100

# Ищем файлы с расширением .py и копируем их содержимое в буфер обмена и отправляем в ChatGPT
for root, dirs, files in os.walk(dir_path):
    # Проверяем, достигнуто ли максимальное количество запросов
    if request_count >= MAX_REQUESTS:
        break

    # Пропускаем папку "venv"
    if 'venv' in dirs:
        dirs.remove('venv')

    for f in files:
        # Проверяем, является ли файл .py и не имеет ли нижних подчеркиваний впереди
        if f.endswith('.py') and not f.startswith('_'):
            # Путь к файлу
            file_path = os.path.join(root, f)

            # Копируем содержимое файла в буфер обмена
            with open(file_path, 'r') as file:
                file_content = file.read()

            # Отправляем содержимое файла в ChatGPT с промптом
            prompt = """You are a helpful assistant that provides code documentation. Please provide a detailed documentation of the following Python code, including comments, docstrings, and type hinting.
                List of RULES for you: 
                ##1 The comments and docstrings should be in Russian. 
                ##2 Add comments with code descriptions per raw or per code block of logic (on your opinion as will be better).
                ##3 You MUST adding similar comments and docstrings everywhere were it is can be and personally filling them.
                ##3 Don't skip any lines from code!
                ##4 Don't forget about additional description comments inside code (# [description]).
                ##5 Add type hinting everywere
                ##6 Don't colapse parts of code for symbols number response economy. You must write whole result code for replace as once instead of unreformatted code from my request!
                ##7 You are can and may Optimize and Clear resulting code as can better.
                ##8 Save each result in your context for learning project and him architecture for better responses in the next answers.

                Code:"""

            try:
                # Отправляем промпт в ChatGPT и включаем file_content в запросе
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that provides code documentation."},
                        {"role": "user", "content": prompt},
                        {"role": "assistant", "content": file_content}
                    ]
                )

                # Увеличиваем счетчик запросов
                request_count += 1

                # Получаем ответ из ChatGPT
                response_text = response.choices[0].message.content.strip()

                # Удаляем начальные и конечные теги кода ```python``` из ответа
                response_text = response_text.removeprefix("```python").removesuffix("```")

                # Добавляем закомментированную документацию в конце ответа
                response_text += "\n\n# Документация"

                # Копируем ответ из ChatGPT в буфер обмена
                pyperclip.copy(response_text)

                # Заменяем содержимое файла ответом из ChatGPT
                with open(file_path, 'w') as file:
                    file.write(f"{file_content}\n\n# Документация:\n\n{response_text}")

                # Выводим результат на экран
                print(f"Содержимое файла {f}:")
                print(pyperclip.paste())

            except openai.error.APIError as e:
                # Обработка ошибки API
                print(f"Ошибка API: {e}")
            except Exception as e:
                # Обработка других ошибок
                print(f"Ошибка: {e}")

# Выводим количество сделанных запросов
print(f"Количество запросов: {request_count}")
