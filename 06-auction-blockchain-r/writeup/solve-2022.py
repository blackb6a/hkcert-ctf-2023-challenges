import hashlib
import random
import re
import time

import requests

url = 'http://localhost:8002'

s = requests.Session()

home = s.get(url).text
for i in home.split('\n'):
    if 'Your address: ' in i:
        my_address = re.search(r'>([\da-f]{32})<', i)[1]
print(f'{my_address=}')
start_time = time.time()

def get_info():
    info = s.get(url + '?info').json()
    return info['time'], info['items']['2'], info['endgame']

def bid(amount, tx_fee=4, item=2):
    nouce = random.randbytes(16).hex()
    data = f'{my_address}{item:04x}{amount:04x}{tx_fee:04x}{nouce}'
    data += hashlib.sha256(data.encode()).digest().hex()
    assert s.get(f'{url}?data={data}').text == '0'

def sleep_until(t):
    now = time.time() - start_time
    assert now < t
    time.sleep(t - now)

print(get_info())
for i in range(0, 180, 15):
    for j in range(5):
        bid(1 if i + j == 0 else 0)
    sleep_until(i + 15)
    print(get_info())
