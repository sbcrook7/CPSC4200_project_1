#!/usr/bin/python3

# Run me like this:
# $ python3 len_ext_attack.py "http://cpsc4200.mpese.com/uniqname/lengthextension/api?token=...."
# or select "Length Extension" from the VS Code debugger

import sys
from urllib.parse import quote
from pysha256 import sha256, padding


class URL:
    def __init__(self, url: str):
        # prefix is the slice of the URL from "http://" to "token=", inclusive.
        self.prefix = url[:url.find('=') + 1]
        self.token = url[url.find('=') + 1:url.find('&')]
        # suffix starts at the first "command=" and goes to the end of the URL
        self.suffix = url[url.find('&') + 1:]

    def __str__(self) -> str:
        return f'{self.prefix}{self.token}&{self.suffix}'

    def __repr__(self) -> str:
        return f'{type(self).__name__}({str(self).__repr__()})'


def main():
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} URL_TO_EXTEND", file=sys.stderr)
        sys.exit(-1)

    url = URL(sys.argv[1])

    #
    # TODO: Modify the URL
    #
    prefix = url.prefix
    token = url.token
    suffix = url.suffix

    padded_token_len = len(str(token)) + len(str(suffix))
    print("Prefix: " + str(prefix))
    print("Token: " + str(token))
    print("Suffix: " + str(suffix))
    print("Padded url len: " + str(padded_token_len))

    m = (str(token) + str(suffix)).encode()

    h1 = sha256()
    h1.update(m)
    print(h1.hexdigest())

    h2 = sha256(state=bytes.fromhex(str(h1.hexdigest())), count=padded_token_len)
    suffix = "command=UnlockSafes".encode()
    h2.update(suffix)
    print(str(prefix) + h2.hexdigest() + str(suffix))
    #url.token = 'TODO'
    #http://cpsc4200.mpese.com/madduxr/lengthextension/api?token=9690858e07b50439d794c771f1b55fb9ee52104f1a66017d55962aaf71b94f68&command=SprinklersPowerOn

    print("URL: " + str(url))


if __name__ == '__main__':
    main()
