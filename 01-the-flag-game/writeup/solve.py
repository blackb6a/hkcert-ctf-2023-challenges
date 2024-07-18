import hashlib
import json
import re
import string

from pwn import wget

url = 'http://127.0.0.1:30001'

js_path = '/js/app.38bf3c86.js'
assert f'src="{js_path}"' in wget(url).decode()

source_map_file = 'app.38bf3c86.js.map'
source_map_path = '/js/' + source_map_file
assert f'# sourceMappingURL={source_map_file}' in wget(url + js_path).decode()

source_map = json.loads(wget(url + source_map_path))
rules_path = 'webpack://the-flag-game/./src/rules.js'
rules_content = source_map['sourcesContent'][source_map['sources'].index(rules_path)]

assert 'u.match(/^hkcert23{.*}$/)' in rules_content
# e.g. sha224(u.substr(0, 8)).startsWith('b08c89')
hash_rule_regex = r'(sha\d{3})\(u\.substr\(0, (\d+)\)\)\.startsWith\(\'([\da-f]+)\'\)'
hash_rules = []
for m in re.finditer(hash_rule_regex, rules_content):
    print(m.group(0))
    algo, end, prefix = m.groups()
    hash_rules.append((getattr(hashlib, algo), int(end), prefix))

def exhaust(s):
    length = len(s)
    if s[-1] == '}':
        for algo, end, prefix in hash_rules:
            b = s[:end].encode()
            if not algo(b).hexdigest().startswith(prefix):
                break
        else:
            print(s)
        return
    length += 1
    for i in string.printable:
        b = (s + i).encode()
        for algo, end, prefix in hash_rules:
            if end == length and not algo(b).hexdigest().startswith(prefix):
                break
        else:
            exhaust(s + i)

exhaust('hkcert23{')
