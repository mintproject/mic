#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 16:17:04 2020

@author: deborahkhider

Simple line model for testing MIC
"""

import json
import sys


if __name__ == "__main__":
    with open(sys.argv[1]) as json_file:
        config=json.load(json_file)
    #open
    dataset_name = config['input']['dataset_name']
    dir_out = config['output']['path']
    a=float(config['params']['a'])
    b=float(config['params']['b'])
    c=float(config['params']['c'])
    with open("outputs.txt", "w") as f:
        f.write(f"{str(a)}\n")
        f.write(f"{str(b)}\n")
        f.write(f"{str(c)}\n")

