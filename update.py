import json
import time
import requests
import datetime

from raven import Client
from requests import Timeout

from api_key import API
from sentry_uri import SENTRY_URI

TYPE_TRAM = 2
TYPE_BUS = 1

TYPES = [TYPE_TRAM, TYPE_BUS]


class FetchError(Exception):
    pass


def fetch_results(type_):
    url = "https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id=f2e5503e-927d-4ad3-9500-4ab9e55deb59&apikey={}&type={}".format(
        API, type_)
    print("try")
    try:
        response = requests.get(url, timeout=3)
    except Timeout:
        raise FetchError("timeout")

    if response.status_code == 200:
        data = response.json()

        if data.get('result') == "B\u0142\u0119dna metoda lub parametry wywo\u0142ania":
            raise FetchError("error in result property")

        if data.get('result', []):
            return data['result']
    else:
        raise FetchError("status_code", response.status_code)


def save_results(results):
    data = {'result': results, 'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    with open("static/bus.json", "w") as f:
        f.write(json.dumps(data))


def main():
    recent_results = {TYPE_TRAM: [], TYPE_BUS: []}

    if SENTRY_URI is not None:
        Client(SENTRY_URI)

    while True:
        for type_ in TYPES:
            try:
                new_results = fetch_results(type_)
            except FetchError as e:
                print(e)
            else:
                recent_results[type_] = new_results
                print(recent_results)
                save_results(recent_results[TYPE_TRAM] + recent_results[TYPE_BUS])

        time.sleep(10)


if __name__ == "__main__":
    main()
