```
openssl req -x509 -newkey rsa:4096 -keyout key_gp3.pem -out cert_gp3.pem -days 365 -nodes
```

``` 
openssl x509 -outform der -in cert.pem -out cert.der
```

cert.conf

```
[req]
default_bits       = 2048
prompt             = no
default_md         = sha256
req_extensions     = req_ext
distinguished_name = dn

[dn]
C  = RU
ST = YourState
L  = YourCity
O  = YourOrganization
OU = YourOrganizationalUnit
CN = 10.136.29.166  # Primary IP address

[req_ext]
subjectAltName = @alt_names

[alt_names]
IP.1 = 10.136.29.166
IP.2 = 10.36.29.5
IP.3 = 192.168.1.19
IP.4 = 10.136.29.162

```

```
openssl genrsa -out key_gp3.pem 2048
```

```
openssl req -new -key key_gp3.pem -out server_gp3.csr -config cert_gp3.conf
```

```
openssl x509 -req -in server_gp3.csr -signkey key_gp3.pem -out cert_gp3.pem -days 1000 -extfile cert_gp3.conf -extensions req_ext
```

```
openssl x509 -in cert_gp3.pem -text -noout
```

```
openssl x509 -outform der -in cert_gp3.pem -out cert_gp3.crt
```