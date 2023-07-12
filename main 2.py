import os
import openai
import pyperclip

# Установите ваш API-ключ ChatGPT
openai.api_key = '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'

# Путь к директории с файлами
dir_path = '/Users/vladglusko/PycharmProjects/pythonProject6/'

# Получаем список файлов в директории
files = os.listdir(dir_path)

# Ищем файлы с расширением .py и копируем их содержимое в буфер обмена и отправляем в ChatGPT
for f in files:
    # Путь к файлу
    file_path = os.path.join(dir_path, f)

    # Проверяем, является ли файл .py
    if os.path.isfile(file_path) and f.endswith('.py'):
        # Копируем содержимое файла в буфер обмена
        with open(file_path, 'r') as file:
            pyperclip.copy(file.read())

        # Отправляем содержимое буфера обмена в ChatGPT с промптом
        prompt = """Please provide a detailed documentation of the following Python code, including comments, docstrings, 
        and type hinting. List of RULES for you: 1 The comments and docstrings should be in Russian. 2 Add comments 
        with code descriptions per raw or per code block of logic (on your opinion as what will be better). 3 You MUST 
        add similar comments and docstrings everywhere it can be and personally fill them. 3 Don't 
        skip any lines of code! 4 Don't forget about additional description comments inside code (# [
        description]). 5 Add type hinting everywhere. 6 Don't collapse parts of code for the sake of saving 
        characters. You must write the entire resulting code to replace it once instead of unreformatted code from my 
        request! 7 You can and may optimize and clean up the resulting code as much as you can. 8 Save each result in your 
        context for the learning project and its architecture for better responses in future answers. This is the 
        selected code: \n```python\n""" + pyperclip.paste() + "\n```"

        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens=100,
            temperature=0.7,
            n=1,
            stop=None,
            timeout=10,
            input=str(pyperclip.paste())
        )

        # Копируем ответ из ChatGPT в буфер обмена
        pyperclip.copy(response.choices[0].text.strip())

        # Выводим результат на экран
        print(f"Содержимое файла {f}:")
        print(pyperclip.paste())
