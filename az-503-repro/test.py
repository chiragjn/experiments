import logging
import requests
import time

logging.basicConfig(level=logging.DEBUG)
URL = "https://..."


def test1(duration):
    s = requests.Session()
    r = s.get(URL + "/no-content")
    r.raise_for_status()
    time.sleep(duration)
    r = s.get(URL + "/no-content")
    r.raise_for_status()


while True:
    test1(1.0 - 0.155)
