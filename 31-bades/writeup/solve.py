from pwn import xor
import requests

def encrypt_flag() -> bytes:
    r = requests.get('http://localhost:28231/encrypt/flag/')
    j = r.json()
    c = bytes.fromhex(j.get('ciphertext'))
    return c

def encrypt(m: bytes) -> bytes:
    r = requests.get('http://localhost:28231/encrypt/', params={
        'm': m.hex()
    })
    j = r.json()
    c = bytes.fromhex(j.get('ciphertext'))
    return c


c1 = encrypt_flag()

flag = b''
for i in range(8, len(c1), 8):
    c2 = encrypt(xor(c1[0:8], c1[i:i+8]))
    flag += xor(c1[i-8:i], c2[8:16])
    print(f'{flag = }')
