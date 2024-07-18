# writeup
Open the pcap file with wireshark

Find this
![image](https://github.com/blackb6a/hkcert-ctf-2023-challenges-internal/assets/33385719/3a424ef7-b537-4a61-a2bc-c5fba98fda1b)
Look at https://github.com/Arno0x/DNSExfiltrator/blob/master/dnsexfiltrator.py

Find this
![image](https://github.com/blackb6a/hkcert-ctf-2023-challenges-internal/assets/33385719/ab570377-15ce-40cf-b374-12f3c761ded4)
Figure out this cook book
```
https://gchq.github.io/CyberChef/#recipe=Find_/_Replace(%7B'option':'Simple%20string','string':'.'%7D,'',true,false,true,false)Find_/_Replace(%7B'option':'Simple%20string','string':'_'%7D,'/',true,false,true,false)Find_/_Replace(%7B'option':'Simple%20string','string':'-'%7D,'%2B',true,false,true,false)RC4(%7B'option':'UTF8','string':'K%232dF!8t@1qZ'%7D,'Base64','Hex')From_Hex('None')Unzip('',false)&input=RU82eWxGbHNVY183dV9RRDhnQkRwOEw4aUZpR1pHa2hwdENfUXduU2VtX2l2ck8zekZVZ2otbmZpOWhNaGdMLmtoVjJVNnRWekpxNUVXbnoteVhaaEJXRm1LTWFLYU02NXFjbGI3N2tGNU1XeFY2bWRWR0R5ajlCZERKUzZ1Qy40OWg0MWVMT05UNVZfVUhna3NNZE9Sb2wtMmNZZ1dreldqNkg2YWU4dVJ6Z1JNSmpEbVlzczhYQk9la3lpYmUudFFWTU5iMjY2OVp6b1JGa0RaV0l5bEJhSjVDTHA4Y28yZ1lIT2dkSURxajdDSUVXa00
```
Submit flag
