from fastapi import FastAPI
import psycopg2
import socket
from threading import Thread
import uvicorn

app = FastAPI(debug=True)

# Параметры подключения к базе данных PostgreSQL
host = 'localhost'
port = '5432'
database = 'new_db'
user = 'postgres'
password = 'password'

# Установка соединения с базой данных
connection = psycopg2.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password
)

# Создание курсора
cursor = connection.cursor()


def handle_client(client_socket):
    request = client_socket.recv(1024).decode()

    # Обработка запроса
    # Можно вызвать соответствующую функцию FastAPI и отправить результат обратно клиенту
    # Пример:
    # response = app(request)
    # client_socket.send(response.encode())

    client_socket.close()


def start_socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.1.103', 8001))
    server_socket.listen(5)

    while True:
        client_socket, address = server_socket.accept()
        client_thread = Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


@app.get("/execute_query/")
def execute_query():
    query = """
    SELECT *
    FROM schema_first.table_name_1
    WHERE ctid = (
        SELECT max(ctid)
        FROM schema_first.table_name_1
    );
    """
    cursor.execute(query)
    result = cursor.fetchone()

    if result is None:
        return {"message": "No records found"}

    result_dict = {"user_name": result[0], "last_name": result[1], "description": result[2]}
    return result_dict


@app.get("/execute_query/{index}")
def execute_query(index: str or int):
    query = f"""
    select t2.*
    from (SELECT t.*, t.ctid
        FROM schema_first.table_name_1 as t
        where t.CTID >= (select schema_first.table_name_1.CTID from schema_first.table_name_1 where schema_first.table_name_1.user_name like '{index}' limit 1)
        limit 2) as t2
    order by t2.CTID DESC
    limit 1;
    """
    cursor.execute(query)
    result = cursor.fetchone()

    if result is None:
        return {"message": "No records found after the provided index"}

    result_dict = {"user_name": result[0], "last_name": result[1], "description": result[2]}
    return result_dict


@app.on_event("startup")
def startup_event():
    # Запуск сервера TCP-сокетов в отдельном потоке
    socket_thread = Thread(target=start_socket_server)
    socket_thread.start()


@app.on_event("shutdown")
def shutdown_event():
    cursor.close()
    connection.close()
    # Завершение сервера TCP-сокетов


# Запуск сервера FastAPI с Uvicorn
if __name__ == "__main__":


    uvicorn.run(app, host="192.168.1.103", port=8000)
