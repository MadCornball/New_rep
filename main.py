import threading
import uvicorn
import psycopg2
import asyncio

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(debug=True)
templates = Jinja2Templates(directory="templates")

# Database connection parameters
host = 'localhost'
port = '5432'
database = 'test_db'
user = 'postgres'
password = 'password'

# Establish connection to the database
connection = psycopg2.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password
)

# Create a cursor to execute queries
cursor = connection.cursor()

# WebSocket соединения
connected_websockets = set()


# Функция проверки разрешения доступа к WebSocket соединениям
async def check_ws_permission(websocket: WebSocket):
    # Здесь можно добавить логику проверки разрешения доступа
    # Например, проверить авторизацию пользователя или другие параметры

    # В данном примере разрешаем всем подключениям
    return True

# Обработчик WebSocket соединения
@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    # Проверяем разрешение доступа
    if not await check_ws_permission(websocket):
        await websocket.close()
        return

    await websocket.accept()
    connected_websockets.add(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            if data == "get_table_data":
                table_data = get_table_data()
                await websocket.send_json({"table_data": table_data})
    except WebSocketDisconnect:
        connected_websockets.remove(websocket)

def get_table_data(table_name=None):
    try:
        if table_name:
            cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'test' AND table_name = %s)", (table_name,))
            if cursor.fetchone()[0]:
                query = f"SELECT * FROM test_db.test.{table_name};"
                cursor.execute(query)
                results = cursor.fetchall()
                if results:
                    data = []
                    column_names = [desc[0] for desc in cursor.description]
                    for result in results:
                        row_data = {}
                        for i in range(len(column_names)):
                            key = column_names[i]
                            value = result[i]
                            if key == 'image':
                                value = '/static/images/'
                            row_data[key] = value
                        data.append(row_data)
                    return data
                else:
                    return []
            else:
                return []
        else:
            query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'test';"
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                table_names = [result[0] for result in results]
                return {"tables": table_names}
            else:
                return []
    except Exception as e:
        print(f"SQL Query Error: {e}")
        return []
    finally:
        connection.commit()


# Отправка данных по сокетам всем подключенным клиентам
async def send_data_to_websockets():
    while True:
        try:
            for websocket in connected_websockets:
                table_data = get_table_data()
                await websocket.send_json({"table_data": table_data})
            await asyncio.sleep(5)  # Пауза между отправками данных (5 секунд в данном примере)
        except Exception as e:
            print(f"Error sending data: {e}")

@app.get("/", response_class=HTMLResponse)
def get_all_tables(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "tables": get_table_data()})

@app.get("/{table_name}/", response_class=HTMLResponse)
def get_table_data_html(request: Request, table_name: str):
    table_data = get_table_data(table_name)
    return templates.TemplateResponse("index.html", {"request": request, "table_data": table_data})

@app.get("/api/{table_name}/")
def get_table_data_api(table_name: str):
    table_data = get_table_data(table_name)
    return table_data

app.mount("/static", StaticFiles(directory="templates/static"), name="static")

if __name__ == "__main__":
    threading.Thread(target=uvicorn.run, args=(app,), kwargs={"host": "192.168.1.6", "port": 8000}).start()
