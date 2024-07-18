from pwn import remote

while True:
    io = remote('localhost', 28103)

    io.recvuntil('📢 '.encode())
    p = int(io.recvlineS(keepends=False))
    print(f'{p=}')

    # 1/3 chance
    if p % 3 == 0:
        io.sendline(str(p // 3).encode())

        io.recvuntil('🤝 '.encode())
        io.send(io.recvline())

        io.recvuntil('🔑 '.encode())
        flag = io.recvlineS(keepends=False)

        # 1/3 chance
        if '🏁 ' in flag:
            print(flag)
            break

    io.close()
