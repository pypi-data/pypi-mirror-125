# !/usr/bin/env python
# -*- coding: utf-8 -*-

import platform
from time import sleep
import sys, traceback

import argparse
from iTude.aopom.chuanbei.visit.flowobject_ import visitAPIMAP

def server_list_object_pickup(name):
    HERE = pathlib.Path(__file__).parent.parent
    buf = ( HERE / "__init__.py" ).read_text()
    slo1 = buf.find(name) + len(f"{name} = ")
    slo2 = buf[slo1:].find("]") + 1
    slo_ = buf[slo1:slo1 + slo2]
    p1 = re.compile("'(.*?)'", re.S)
    return (re.findall(p1, slo_))


def get_platform():
    return platform.platform()


def get_node():
    return platform.node()


def maintude(args):
    print("")
    print("--cmaddress {0}".format(args.cmaddress))


def itude_app():
    parser = argparse.ArgumentParser(usage="it's usage on the chinesemadrine address port.", description="help info.")
    parser.add_argument("-C", "--cmaddress", default="cmaddress", help="the chinese madrine address input.")
    args = parser.parse_args()
    maintude(args)
    print(args.cmaddress)
    visitAPIMAP(args.cmaddress)



