import requests
import hashlib
import hmac
import time
import websocket
import json

API_KEY = 'qk0suc02SENu0ePE7ZtV0aSudCdXRdPUnz1VhiuJWIBlkEJOFYYK5MxoqzGwzJri'
API_SECRET = 'VGELzsvP1NyIfl2ciNpxddlyh2xvC5qTs9J8AwsxxMOKBrHWp8QtwUVT8DaY26Tx'

BASE_URL = 'https://api.binance.com'


def on_message(ws, message):
    data = json.loads(message)
    print(data)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("Closed")

def on_open(ws):
    print("Connected")
    payload = {
        "method": "SUBSCRIBE",
        "params": [
            # f"btcusdt@trade",  # Для сделок
            f"btcusdt@ticker"  # Для котировок

        ],
        "id": 1
    }
    ws.send(json.dumps(payload))



def create_signature(params):
    timestamp = int(time.time() * 1000)
    signature_payload = '&'.join([f'{k}={v}' for k, v in params.items()])
    signature_payload += f'&timestamp={timestamp}'

    signature = hmac.new(API_SECRET.encode('utf-8'), signature_payload.encode('utf-8'), hashlib.sha256).hexdigest()
    return timestamp, signature

def create_signed_request(method, endpoint, params={}):
    timestamp, signature = create_signature(params)

    headers = {
        'X-MBX-APIKEY': API_KEY
    }

    if method == 'GET':
        response = requests.get(f'{BASE_URL}{endpoint}', headers=headers, params=params)
    elif method == 'POST':
        params['timestamp'] = timestamp
        params['signature'] = signature
        response = requests.post(f'{BASE_URL}{endpoint}', data=params, headers=headers)

    return response.json()

def place_buy_order(symbol, buy_quantity, buy_price):
    endpoint = '/api/v3/order'
    params = {
        'symbol': symbol,
        'side': 'BUY',
        'type': 'LIMIT',
        'timeInForce': 'GTC',
        'quantity': buy_quantity,
        'price': buy_price
    }
    return create_signed_request('POST', endpoint, params)

def place_sell_order(symbol, sell_quantity, sell_price):
    endpoint = '/api/v3/order'
    params = {
        'symbol': symbol,
        'side': 'SELL',
        'type': 'LIMIT',
        'timeInForce': 'GTC',
        'quantity': sell_quantity,
        'price': sell_price
    }
    return create_signed_request('POST', endpoint, params)

def get_klines_data(symbol, interval):
    endpoint = '/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': interval
    }
    response = requests.get(f'{BASE_URL}{endpoint}', params=params)
    return response.json()

if __name__ == '__main__':
    buy_symbol = 'BTCUSDT'
    sell_symbol = 'BTCUSDT'
    interval = '1h'
    buy_quantity = 0.001
    sell_quantity = 0.001
    buy_price = 45000.0
    sell_price = 45000.0
    klines_data = get_klines_data(buy_symbol, interval)
    url = "wss://stream.binance.com:9443/ws/btcusdt@indexPrice"
    ws = websocket.WebSocketApp(url, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
    print(place_buy_order(buy_symbol, buy_quantity, buy_price))
    print(place_sell_order(sell_symbol, sell_quantity, sell_price))

    print("Klines Data:", klines_data)