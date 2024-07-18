from pwn import *
import math

def clean(n):
    while n % 2 == 0: n //= 2
    for k in range(3, 100000, 2):
        while n % k == 0:
            n //= k
    return n

def encrypt(r, m):
    r.sendlineafter('🤖 '.encode(), f'encrypt {m}'.encode())
    r.recvuntil('🔑 '.encode())
    return int(r.recvline())

def decrypt(r, c):
    r.sendlineafter('🤖 '.encode(), f'decrypt {c}'.encode())
    r.recvuntil('🔑 '.encode())
    return int(r.recvline())

# ~100s
def main():
    # r = process(['python3', 'chall.py'])
    r = remote('chal.hkcert23.pwnable.hk', 28108)

    r.recvuntil('🏁 '.encode())
    c0 = int(r.recvline())

    e = 65537

    m1 = 2**2048
    c1 = encrypt(r, m1)

    c2 = c1
    m2 = decrypt(r, c2)

    p_times_q = clean(m1 - m2)

    m3 = decrypt(r, 2**e)

    _q = math.gcd(Integer(pow(m3, e**2, p_times_q) - 2), p_times_q)
    print(f'{_q = }')

    assert p_times_q % _q == 0
    _p = p_times_q // _q
    print(f'{_p = }')

    # m -> s -> t -> c
    s3 = Integer(pow(m3, e, _p*_q))

    u = s3**e - 2 # <-- bottleneck 1

    s2 = Integer(pow(m2, e, _p*_q))
    v = Integer(pow(s2, e, u)) # <-- bottleneck 2
    w = Integer(pow(v, e, u)) - c2 # <-- bottleneck 3

    # u, v, w are ~2048*65537 bits long

    # XXX: sometimes gcd(u, w) = 1... not sure why yet but just reconnect
    _r = clean(gcd(u, w))
    print(f'{_r = }')

    n = _p * _q * _r
    phi = (_p-1) * (_q-1) * (_r-1)
    d = int(pow(e, -1, phi))
    t0 = int(pow(c0, d, _r*_p))
    s0 = int(pow(t0, d, _q*_r))
    m0 = int(pow(s0, d, _p*_q))

    flag = int.to_bytes(m0, (m0.bit_length()+7)//8, 'big')
    print(f'{flag = }')

if __name__ == '__main__':
    main()