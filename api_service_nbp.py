import requests
import csv

def get_write_rates():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()

    with open('kursy.csv', 'w') as csvfile:
        fieldnames = ['currency', 'code', 'bid', 'ask']
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        csvwriter.writeheader()

        for n in data[0]["rates"]:
            csvwriter.writerow(n)

if __name__ == '__main__':
    get_write_rates()



