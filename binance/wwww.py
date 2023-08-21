from fastapi import FastAPI, WebSocket
import asyncio
import json
import websockets

app = FastAPI()

# Список WebSocket-подключений
connections = []

# WebSocket-обработчик
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Здесь вы можете добавить логику обработки полученных данных
    except:
        connections.remove(websocket)
# API_KEY = "qmFbBVdDyAtLg2GV6tgSNoFOPHDznKkrXZ2t0kO7mgVpO4Q9EbwmFjEdsO8U2y9R"
# SECRET_KEY = "eqBMTZLnouSOgN0d0y1Mxrh1YFK7zIBozGmitqvAdyBCt3yKaeIOJv1dvRptQA9h"

# Запуск сервера с WebSocket-поддержкой
@app.websocket("/ws")
async def websocket_handler(websocket: WebSocket):
    await websocket_endpoint(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
