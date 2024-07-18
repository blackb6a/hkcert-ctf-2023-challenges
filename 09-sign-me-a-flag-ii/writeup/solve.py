import hmac
import hashlib
from rich.progress import track
from pwn import *

# context.log_level = 'debug'

def sign_message(id: int, key_client: bytes, key_server: bytes, message: str) -> bytes:
    key_combined = xor(key_client, key_server)
    full_message = f'{id}{message}'.encode()

    signature = hmac.new(key_combined, full_message, hashlib.sha256).digest()
    return signature

def _sign_send(r, key_client: bytes, message: str):
    r.sendline(b'sign')
    r.sendline(key_client.hex().encode())
    r.sendline(message.encode())

def _sign_recv(r):
    r.recvuntil('📝 '.encode())
    return bytes.fromhex(r.recvline().decode().strip())

def sign(r, key_client: bytes, message: str):
    _sign_send(r, key_client, message)
    return _sign_recv(r)

def get_flag(r, key_server: bytes, id: int):
    signature = sign_message(id, b'', key_server, 'gib flag pls')

    r.sendlineafter('🎬 '.encode(), b'verify')
    r.sendlineafter('💬 '.encode(), b'gib flag pls')
    r.sendlineafter('📝 '.encode(), signature.hex().encode())

def get_reference_id(t):
    while t % 10 == 0: t //= 10
    return t

def get_target_zeroes(t, N):
    p = 0
    while t*10 < N: t, p = t*10, p+1
    return p

if __name__ == '__main__':
    N = 65536

    # r = process(['python3', 'chall.py'])
    r = remote('chal.hkcert23.pwnable.hk', 28009)

    signatures = {}

    key_server = b''

    results = []

    s = 0
    for i in range(16): # we are going to recover the i-th byte of `key_server`
        u = 0
        pairs = []
        while u < 256:
            if s > 0 and s % 10 == 0:
                # If there is a reference for this message...
                t = get_reference_id(s)
                p = get_target_zeroes(s, N)

                message = '0'*p + 'test'
                key_client = b'\0'*16 + key_server + bytes([u])
                _sign_send(r, key_client, message)
                u += 1
                pairs.append((s, t))
            elif s > 0 and s*10 < N:
                # If this message can be used for future reference...
                p = get_target_zeroes(s, N)

                message = '0'*p + 'test'
                _sign_send(r, b'\0'*16, message)
            else:
                _sign_send(r, b'', 'whatever...')

            s += 1

            # Read from server if we are lagging behind for too long
            if s - len(results) == 1024:
                while len(results) < s:
                    results.append(_sign_recv(r))

        # Read from server...
        while len(results) < s:
            results.append(_sign_recv(r))

        for u, (s1, t1) in enumerate(pairs):
            if results[s1] != results[t1]: continue
            key_server += bytes([u])
            break
        print(f'{key_server = }')

    get_flag(r, key_server, s)
    
    r.interactive()
