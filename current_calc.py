from flask import Flask, request, render_template
import requests

app = Flask(__name__)

exchange_rates = []

def fetch_exchange_rates():
    global exchange_rates
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    exchange_rates = data[0]['rates']

fetch_exchange_rates()

@app.route("/", methods=['GET', 'POST'])
def curr_calc():
    global exchange_rates
    
    if request.method == 'GET':
        codes = [c["code"] for c in exchange_rates]
        return render_template("calc_form.html", codes=codes) 
    
    elif request.method == 'POST':
        select_curr = request.form.get("currencies")
        exchange_amount = float(request.form.get("element"))
        
        for rate in exchange_rates:
            if rate["code"] == select_curr:
                select_bid = rate["bid"]
                break
        
        transaction_cost = select_bid * exchange_amount
       
        codes = [c["code"] for c in exchange_rates]
        return render_template("calc_form.html", codes=codes, transaction_cost=transaction_cost)