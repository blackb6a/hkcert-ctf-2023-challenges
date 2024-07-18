from pwn import *
import ast
from rich.progress import track

def connect():
    # return process(['python3', 'chall.py'])
    return remote('chal.hkcert23.pwnable.hk', 28128)

def decrypt(r, c):
    r.sendline(str(c).encode())
    r.recvuntil('🤫 '.encode())
    return int(r.recvline().decode())


def main():
    # Idea:
    # 1. connect to the server for the first time, use the "padding oracle" to find the length of the flag
    # 2. replace `h` by 0x00 and recover the flag byte-by-byte
    flag_length = get_flag_length()
    print(f'{flag_length = }')
    flag = recover_flag(flag_length)
    print(f'{flag = }')


def get_flag_length():
    r = connect()
    r.recvuntil('📢 '.encode())
    n, g = ast.literal_eval(r.recvline().decode())
    r.recvuntil('🏁 '.encode())
    c0 = int(r.recvline().decode())

    for i in track(range(2048//8)):
        try:
            # c1 is a ciphertext of m + 256^i
            c1 = c0 * pow(g, 256**i, n**2) % n**2
            decrypt(r, c1)
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            r.close()
            return i

def recover_flag(flag_length):
    r = connect()
    r.recvuntil('📢 '.encode())
    n, g = ast.literal_eval(r.recvline().decode())
    r.recvuntil('🏁 '.encode())
    c0 = int(r.recvline().decode())

    n2 = n**2
    k = pow(2, -1, n)

    # adjustment for padding
    Δm  = 0x01 * 256**(2048//8 - 2) # makes "00 01 xx xx ..." to "00 02 xx xx ...."
    Δm += 0x80 * 256**(2048//8 - 3) # sets the first bit of the third byte to be 1, to avoid null bytes inside paddings

    # c1 is now is a ciphertext of "\0kcert23{...}"
    m = b'h' + b'\0'*(flag_length-1)
    m = int.from_bytes(m, 'big')
    c1 = pow(g, -m, n2) * c0 % n2

    for i in range(flag_length*8 - 8):
        mb = decrypt(r, c1)

        m += mb<<i
        flag = int.to_bytes(m, flag_length, 'big')
        print(f'{i}/{flag_length*8-8}: {flag = }')

        # m -> m-mb
        c1 = pow(g, -mb, n2) * c1 % n2
        # m -> m//2
        c1 = pow(c1, k, n2)
        # adjust padding
        c1 = pow(g, Δm, n2) * c1 % n2

    r.close()
    return flag


if __name__ == '__main__':
    main()
