from flask import Flask, request, render_template
import requests

app = Flask(__name__)

def get_exchange_rates():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    return data[0]['rates']

@app.route("/", methods=['GET', 'POST'])
def curr_calc():
    codes = [c["code"] for c in get_exchange_rates()]
    if request.method == 'GET':
        return render_template("calc_form.html", codes=codes) 
    
    elif request.method == 'POST':
        select_curr = request.form.get("currencies")
        exchange_amount = float(request.form.get("element"))
        
        for i in get_exchange_rates():
            if i["code"] == select_curr:
                select_bid = i["bid"]
                
        transaction_cost = select_bid * exchange_amount
       
        return render_template("calc_form.html", codes=codes, transaction_cost=transaction_cost) 
    
