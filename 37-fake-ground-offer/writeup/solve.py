import requests, re, time

print("just wait")
# brute (or brush?) first 10 draws
while True:
  r = requests.get("http://localhost:8804/?gacha10=Summon+10")
  ur = re.search("\[UR\] => ([0-9]+)", r.text)
  ssr = re.search("\[SSR\] => ([0-9]+)", r.text)
  cookie = r.headers["Set-Cookie"] # you can also get it from the "Master's ID"
  sid = cookie.split("=")[1]
  if(int(ur[1]) + int(ssr[1]) != 10):
    time.sleep(1)
  else:
    print(sid)
    break

time.sleep(355*2) # magic number for next gacha
r = requests.get("http://localhost:8804/?gacha10=Summon+10",cookies={"PHPSESSID":sid})
print(r.text)
r = requests.get("http://localhost:8804/?sellacc",cookies={"PHPSESSID":sid})
print(r.text)

'''
# no one cares since the result may be different in php lol
import math

class RNG:
  def __init__(self, seed):
    self.s0 = float(seed)
    self.s1 = float(seed)

  def __iter__(self):
    while True:
      x = math.sin(self.s0)
      self.s0 += self.s1
      yield x-math.floor(x)

for j in range(1,6):
  s = 355*2 * j
  print(s)
  print("-----")
  f = RNG(s)
  for i, v in enumerate(f, 1):
      print(v)
      if i >= 10:
          break
  print("-----")
'''
