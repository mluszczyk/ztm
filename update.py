import json
import time
import requests
import datetime

from api_key import API

from requests import Timeout


def main():
    while True:
        url = "https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id=f2e5503e-927d-4ad3-9500-4ab9e55deb59&apikey={}&type=1".format(
            API)
        print("try")
        try:
            response = requests.get(url,
                                    timeout=3)
        except Timeout:
            print("timeout")

        if response.status_code == 200:
            data = response.json()

            if data.get('result') == "B\u0142\u0119dna metoda lub parametry wywo\u0142ania":
                print("error in result property")
                continue

            if data.get('result', []):
                data['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open("static/bus.json", "w") as f:
                    f.write(json.dumps(data))
        else:
            print("status_code", response.status_code)

        time.sleep(10)

main()
