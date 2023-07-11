import openai
import pyautogui
import pyperclip
import time
import concurrent.futures
import io

# Установите ваш API-ключ ChatGPT
openai.api_key = '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'
prompt = """Please provide a detailed documentation of the following Python code, including comments, docstrings, 
and type hinting. List of RULES for you: 1 The comments and docstrings should be in Russian. 2 Add comments 
with code descriptions per raw or per code block of logic (on your opinion as what will be better). 3 You MUST 
add similar comments and docstrings everywhere it can be and personally fill them. 3 Don't 
skip any lines of code! 4 Don't forget about additional description comments inside code (# [
description]). 5 Add type hinting everywhere. 6 Don't collapse parts of code for the sake of saving 
characters. You must write the entire resulting code to replace it once instead of unreformatted code from my 
request! 7 You can and may optimize and clean up the resulting code as much as you can. 8 Save each result in your 
context for the learning project and its architecture for better responses in future answers. This is the 
selected code: \n```python\n\n```"""
# Открываем файл в PyCharm Finder
def open_file(filename):
    pyautogui.run(f"h'shiftleft,win,O'w'{filename}'k'enter'")


# Отправляем содержимое файла в ChatGPT
def send_to_chatgpt(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,
        n=1,
        stop=None,
        timeout=10
    )
    return response.choices[0].text.strip()

# Пример использования функций для открытия файла, копирования содержимого и отправки в ChatGPT
filename = 'open /Users/vladglusko/PycharmProjects/pythonProject6/qwettttt.py'  # Замените на путь к вашему файлу
open_file(filename)


def replace_in_line(line):
    return line.replace('old_substring', '/path/to/new_substring')

with io.open(filename, 'r') as f:
    
    with io.open('output', 'w', buffering=10000) as out:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for result in executor.map(replace_in_line, f):
                out.write(result)

content = ...

response = send_to_chatgpt(prompt)
print(response)
