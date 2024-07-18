from pwn import *

# context.log_level = 'debug'

def attempt():
    # r = process(['python3', 'chall.py'])
    r = remote('localhost', 28103)

    r.recvuntil('📢 '.encode())
    p = int(r.recvline().decode())

    if p % 3 != 0:
        r.close()
        return False
    x = p//3

    r.sendlineafter('👋 '.encode(), str(x).encode())

    r.recvuntil('🤝 '.encode())
    y = int(r.recvline().decode())
    k = y

    r.sendlineafter('🔑 '.encode(), str(k).encode())

    res = r.recvline().decode().strip()
    r.close()

    if res == '😒':
        return False
    print(res)

    return True

def main():
    while not attempt(): pass


if __name__ == '__main__':
    main()