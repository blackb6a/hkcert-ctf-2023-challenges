# Find a combination C(n1, r1) + C(n2, r2) + ... = 10^9 + 7

# Use greedy!
BDD  = 10**9 + 7
BDD -= binomial(97, 6)
BDD -= binomial(69, 5)
BDD -= binomial(39, 5)
BDD -= binomial(44, 3)
BDD -= binomial(16, 2)
BDD -= binomial(5, 1)

ncrs = []
for n in range(100):
    for r in range(n//2):
        ncr = binomial(n, r)
        if ncr > BDD: continue
        ncrs.append((ncr, n, r))
    
ncrs = sorted(ncrs, reverse=True)

print(f'{BDD = }')
for ncr in ncrs[:10]:
    print(ncr)