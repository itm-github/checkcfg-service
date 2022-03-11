#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import yaml
import sys

wd = os.path.dirname(sys.argv[0])
os.chdir(wd)

# читаем конфиг
with open('chkcfgServiceConfig.yaml', encoding="utf-8") as fp:
    CONFIG = yaml.load(fp, Loader=yaml.FullLoader)