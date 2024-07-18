from pwn import *
from rich.progress import track
from Crypto.Util.Padding import unpad

HEXCHARS = b'0123456789abcdef'

oracle_calls = 0
def read(r):
    r.recvuntil('🔑 '.encode())
    return bytearray.fromhex(r.recvline().decode())

def _aes_to_rsa_send(r, t: bytearray) -> bytearray:
    global oracle_calls
    oracle_calls += 1
    r.sendline(f'aes {t.hex()}'.encode())

def _rsa_to_aes_send(r, s: bytearray) -> bytearray:
    global oracle_calls
    oracle_calls += 1
    r.sendline(f'rsa {s.hex()}'.encode())

def rsa_to_aes(r, s):
    _rsa_to_aes_send(r, s)
    return read(r)

def aes_to_rsa(r, s):
    _aes_to_rsa_send(r, s)
    return read(r)

def xor(a, b):
    return bytearray(u^v for u, v in zip(a, b))

def forge_aes_ciphertext(m: bytearray, m0: bytearray, c0: bytearray):
    '''Forge a two-block ciphertext that is Encrypted(m)

    Args:
        m: The target plaintext block
        m0: The corresponding plaintext such that c0 = AES-ECB(m0).
        c0: The corresponding ciphertext such that c0 = AES-ECB(m0).
    '''
    assert len(m) == len(m0) == len(c0) == 16
    return xor(m, m0) + c0

def recover_block(r, m1: bytearray, c1: bytearray, m0: bytearray, c0: bytearray):
    '''Recover x such that AES-ECB(x) = c1, knowing that 
        - aesu such that AES-CBC(u) = m1+c1 consists of all hex chars, and
        - AES-CBC([16 null bytes]) = m0+c0.
    '''
    m = bytearray(16)

    assert len(c0) == len(c1) == len(m0) == len(c0) == 16
    for k in track(range(16)):
        # Create a plaintext with 16-k byte padding (in PKCS7)
        t_suffix = forge_aes_ciphertext(bytearray([16-k for _ in range(16)]), m0, c0)
        
        iv = bytearray(16)

        for i in range(k):
            iv[i] = m[i]

        for u in HEXCHARS[:15]:
            iv[k] = m1[k] ^ u
            t0 = iv + c1 + t_suffix
            _aes_to_rsa_send(r, t0)
        
        ss = [read(r) for _ in range(15)]
        for s0 in ss:
            _rsa_to_aes_send(r, s0)

        ts = [len(read(r)) for _ in range(15)] + [48]

        m[k] = m1[k] ^ HEXCHARS[ts.index(48)]

    return xor(m1, m)


def recover(r, c: bytearray, m0: bytearray, c0: bytearray):
    m = b''
    for i in range(0, 128, 16):
        m += recover_block(r, c[i:i+16], c[i+16:i+32], m0, c0)
        print(f'{m = } ({oracle_calls = })')
    return m


def main():
    # r = process(['python3', 'chall.py'])
    r = remote('chal.hkcert23.pwnable.hk', 28221)

    t0 = read(r)

    t1 = rsa_to_aes(r, b'\0')
    m0, c0 = xor(t1[0:16], bytes.fromhex('000f0f0f 0f0f0f0f 0f0f0f0f 0f0f0f0f')), t1[16:32]

    secret = recover(r, t0, m0, c0)

    r.sendline(f'easy {secret.hex()}'.encode())

    print(f'{oracle_calls = }')
    print(r.recvline().decode().strip())


if __name__ == '__main__':
    main()