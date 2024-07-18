# ii = b"internal{s1mpl3_py3.12_f14g_ch3ck3r}"
bb = b'\xdc\xa0\xe3\xd6\xe2\x9e\xc6\xde\xe7\xefr\x9d\xef\x92\xaa\xc0\xcc\x9b\x80\xb0\x99\x9c\x80\xa8\x9c^\xea\xb4\xeb\xa8\x8c\xef\xbf\x87\x87\x95'
kk = b"s1mpl3_stu77"

flag = b""
for i, x in enumerate(bb):
    c = kk[i % len(kk)]
    x -= c
    x ^= i
    x %= 256
    flag += bytes([x])

print(flag)
