#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from iTude.z_core import get_node, get_platform, itude_app

try:

   from pystarmeow_cryptor.pystarmeow_cryptor_ import check_license

except ImportError:

   try:

       command_to_execute = "pip install PYSTARMEOWCRYPTOR || easy_install PYSTARMEOWCRYPTOR"

       os.system(command_to_execute)

   except OSError:

       print ("Can NOT install pystarmeow_cryptor, Aborted!")

       sys.exit(1)

   from pystarmeow_cryptor.pystarmeow_cryptor_ import check_license


def run():
    itude_app()

'''
def run():
    if check_license():
        print('程序继续运行！')
        print(get_node())
        print(get_platform())
        itude_app()
    else:
        print('程序授权终止，退出！')
'''

