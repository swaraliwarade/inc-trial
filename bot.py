import os, time, hmac, hashlib, requests
from dotenv import load_dotenv
from indicators import compute_indicators

load_dotenv()

BASE_URL = "https://api.coindcx.com"
API_KEY = os.getenv("COINDCX_API_KEY")
API_SECRET = os.getenv("COINDCX_API_SECRET").encode()

def sign_payload(payload):
    import json, time
    payload["timestamp"] = int(round(time.time() * 1000))
    signature = hmac.new(API_SECRET, json.dumps(payload).encode(), hashlib.sha256).hexdigest()
    return signature, payload

def get_candles(symbol="BTCUSDT", interval="5m", limit=50):
    url = f"{BASE_URL}/exchange/v1/markets/candles?pair={symbol}&interval={interval}&limit={limit}"
    r = requests.get(url)
    return r.json()

def place_order(side, symbol="BTCUSDT", qty=0.001, price=None):
    url = f"{BASE_URL}/exchange/v1/orders/create"
    body = {
        "side": side,  # "buy" or "sell"
        "order_type": "market",
        "market": symbol,
        "total_quantity": qty
    }
    sig, signed_body = sign_payload(body)
    headers = {"X-AUTH-APIKEY": API_KEY, "X-AUTH-SIGNATURE": sig}
    r = requests.post(url, json=signed_body, headers=headers)
    return r.json()

def strategy():
    candles = get_candles("BTCUSDT", "5m", 100)
    df = compute_indicators(candles)
    latest = df.iloc[-1]

    if latest["rsi"] < 30 and latest["ema12"] > latest["ema26"]:
        print("Signal: BUY")
        # place_order("buy")
    elif latest["rsi"] > 70 and latest["ema12"] < latest["ema26"]:
        print("Signal: SELL")
        # place_order("sell")
    else:
        print("No trade")

if __name__ == "__main__":
    while True:
        try:
            strategy()
        except Exception as e:
            print("Error:", e)
        time.sleep(60)  # run every 1 min
