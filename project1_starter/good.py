#!/usr/bin/python3
# coding: latin-1
blob = """                 �
'��_z���b��m�Aʻ��9�@A.�-����P淜odC�Mm�.�#�=����u�-�j�ɰ���5�5.ȶ�E}AN��,���y��oà�EvWz���\%kq�J1Xde �c"""
from hashlib import sha256
if sha256(blob.encode("latin-1")).hexdigest() == 'c17646cd0cdd39d0dcc740850bc7f559ff98f798816761a6fe1f4e1f568dbae3':
    print("MD5 is perfectly secure!")
else:
    print("Use SHA-256 instead!")