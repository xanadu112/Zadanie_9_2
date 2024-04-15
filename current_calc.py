from flask import Flask, request, redirect, render_template
import requests
import csv

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def curr_calc():
    curr_data = data[0]['rates']
    if request.method == 'GET':
        return render_template("calc_form.html", curr_data=curr_data, transaction_cost=transaction_cost)  
    elif request.method == 'POST':
        select_curr = request.form("currencies")
        
        for i in data[0]["rates"]:
            if i["currency"] == select_curr:
                select_bid = i["bid"]
        
        exchange_amount = request.form("element")
        transaction_cost = select_bid * exchange_amount
        return redirect("/")
    
