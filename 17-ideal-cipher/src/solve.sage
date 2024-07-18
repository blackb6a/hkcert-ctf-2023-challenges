import itertools
from pwn import xor

BLOCK_SIZE = 2

def xor(a, b):
    return bytes(u^^v for u, v in zip(a, b))

with open('transcript.txt') as f:
    ciphertexts = f.read().strip().split('\n')

len_padded_message = len(bytes.fromhex(ciphertexts[0])) - BLOCK_SIZE

solns = []
for ciphertext in ciphertexts:
    ciphertext = bytes.fromhex(ciphertext)
    for i, j in itertools.combinations(range(0, len(ciphertext)-BLOCK_SIZE, BLOCK_SIZE), r=2):
        if ciphertext[i+BLOCK_SIZE:i+2*BLOCK_SIZE] == ciphertext[j+BLOCK_SIZE:j+2*BLOCK_SIZE]:
            xorred = xor(ciphertext[i:i+BLOCK_SIZE], ciphertext[j:j+BLOCK_SIZE])
            solns.append((i, j, xorred))

A, b = [], []

for i, j, xorred in solns:
    for k in range(16):
        _A = [0 for _ in range(len_padded_message*8)]
        _b = 0

        _A[8*i+k] = _A[8*j+k] = 1
        _b = int.from_bytes(xorred, 'big')>>(15-k)

        A.append(_A)
        b.append(_b)

A = Matrix(GF(2), A)
b = vector(GF(2), b)

x0 = A.solve_right(b)

l = 1337

soln = [int(x) for x in x0]
soln = soln[::-1]
soln = sum(s<<i for i, s in enumerate(soln))
soln = int.to_bytes(soln, len_padded_message, 'big')

# The odd part of the flag
for i in range(256):
    flag = bytes(s^^i for s in soln[0::2])
    if max(flag) >= 0x80: continue
    print(flag)
    
print()

# The even part of the flag
for i in range(256):
    flag = bytes(s^^i for s in soln[1::2])
    if max(flag) >= 0x80: continue
    print(flag)
