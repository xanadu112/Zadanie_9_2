from flask import Flask, request, render_template
import requests
import csv
import os

app = Flask(__name__)

CSV_FILE = 'exchange_rates.csv'

def fetch_exchange_rates():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()[0]['rates']
    with open(CSV_FILE, 'w', newline='') as csvfile:
        fieldnames = ['code', 'bid']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for rate in data:
            writer.writerow({'code': rate['code'], 'bid': rate['bid']})

if not os.path.exists(CSV_FILE):
    fetch_exchange_rates()

exchange_rates = {}
with open(CSV_FILE, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        exchange_rates[row['code']] = float(row['bid'])

@app.route("/", methods=['GET', 'POST'])
def curr_calc():
    if request.method == 'GET':
        codes = list(exchange_rates.keys())
        return render_template("calc_form.html", codes=codes) 
    
    elif request.method == 'POST':
        select_curr = request.form.get("currencies")
        exchange_amount = float(request.form.get("element"))
        
        select_bid = exchange_rates.get(select_curr)
        if select_bid is None:
            return "Kod waluty nieprawidłowy"
                
        transaction_cost = select_bid * exchange_amount
       
        codes = list(exchange_rates.keys())
        return render_template("calc_form.html", codes=codes, transaction_cost=transaction_cost)