from flask import Flask, jsonify
import yfinance as yf
import time

app = Flask(__name__)

@app.route('/spy')
def get_spy_price():
    ticker = yf.Ticker("SPY")
    hist = ticker.history(period="1d")  # Haal data voor de laatste dag op
    price = hist['Close'].iloc[-1]  # Haal het sluitend prijspunt

    return jsonify({
        'symbol': "SPY",
        'price': float(price)
    })

if __name__ == '__main__':
    print(f"Run app, start time: {time.ctime(time.time())}")
    app.run(host='0.0.0.0', port=5100)
    print(f"finished {time.ctime(time.time())}")