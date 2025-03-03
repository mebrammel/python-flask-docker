# Import libraries
from flask import Flask, request, jsonify
import yfinance as yf
import pandas as pd
import json


# Define functions
app = Flask(__name__)

def fetch_option_data(symbol='SPY'):
    # Maak een Ticker-object aan voor het opgegeven symbool
    ticker = yf.Ticker(symbol)   
    # Haal alle vervaldatums op
    expiration_dates = ticker.options    
    # Initialiseer een dictionary om alle optiegegevens op te slaan
    options_data = {}
    # Loop over elke vervaldatum
    for date in expiration_dates:
        # Haal de optiegegevens voor de huidige vervaldatum op
        option_chain = ticker.option_chain(date)        
        # Converteer de call en put DataFrames naar dictionaries
        calls = option_chain.calls.to_dict(orient='records')
        puts = option_chain.puts.to_dict(orient='records')        
        # Converteer datumkolommen naar stringformaten
        for option_list in [calls, puts]:
            for option in option_list:
                for key, value in option.items():
                    if isinstance(value, pd.Timestamp):
                        option[key] = value.strftime('%Y-%m-%d %H:%M:%S')       
        # Voeg de geconverteerde data toe aan de options_data dictionary
        options_data[date] = {'calls': calls, 'puts': puts}
    # Retourneer de verzamelde data als een JSON-object
    return json.dumps(options_data, indent=4)

def ticker_profile(symbol="SPY"):
    ticker = yf.Ticker(symbol)
    results = {}
    results["cashflow"] = ticker.cashflow.to_json()
    results["balance_sheet"] = ticker.balance_sheet.to_json()
    results["financials"] = ticker.financials.to_json()
    results["dividends"] = ticker.dividends.to_json()
    results["actions"] = ticker.actions.to_json()
    results["history"] = ticker.history().to_json()
    results["info"] = ticker.info
    return results
    
# Define API Endpoints

@app.route('/api/options', methods=['GET']) # http://192.168.178.170:7300/api/options?symbol=spy
def get_option_chain():
    symbol = request.args.get('symbol', 'SPY').upper()
    try:
        options_data = fetch_option_data(symbol)
        return options_data, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/price', methods=['GET']) # http://192.168.178.170:7300/api/price?symbol=spy
def get_price():
    symbol = request.args.get('symbol', 'SPY').upper()
    try:
        ticker = yf.Ticker(symbol)
        return ticker.history(period="max").to_json(), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile', methods=['GET']) # http://192.168.178.170:7300/api/profile?symbol=spy
def get_ticker_profile():
    symbol = request.args.get('symbol', 'SPY').upper()
    try:
        return ticker_profile(symbol), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)