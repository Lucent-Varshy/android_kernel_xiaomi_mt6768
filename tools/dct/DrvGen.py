#! /usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (C) 2016 MediaTek Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See http://www.gnu.org/licenses/gpl-2.0.html for more details.

import os
import sys
import getopt
import traceback
import subprocess
import xml.dom.minidom

sys.dont_write_bytecode = True

sys.path.append('.')
sys.path.append('..')

from obj.ChipObj import ChipObj
from obj.ChipObj import MT6797, MT6757, MT6757_P25, MT6570, MT6799, MT6759, MT6763
from obj.ChipObj import MT6750S, MT6758, MT6739, MT8695, MT6771, MT6775, MT6779
from obj.ChipObj import MT6768, MT6785
from utility.util import LogLevel, log

def usage():
    print('''
usage: DrvGen [dws_path] [file_path] [log_path] [paras]...

options and arguments:

dws_path    :    dws file path
file_path   :    where you want to put generated files
log_path    :    where to store the log files
paras       :    parameter for generate wanted file
''')

def is_oldDws(path, gen_spec):
    if not os.path.exists(path):
        log(LogLevel.error, f'Cannot find {path}')
        sys.exit(-1)

    try:
        root = xml.dom.minidom.parse(dws_path)
    except Exception as e:
        log(LogLevel.warn, f'{dws_path} is not XML format, try to use old DCT!')
        if len(gen_spec) == 0:
            log(LogLevel.warn, 'Please use old DCT UI to generate all files!')
            return True
        old_dct = os.path.join(sys.path[0], 'old_dct', 'DrvGen')
        cmd = f'{old_dct} {dws_path} {gen_path} {log_path} {gen_spec[0]}'
        if subprocess.call(cmd, shell=True) == 0:
            return True
        else:
            log(LogLevel.error, f'{dws_path} format error!')
            sys.exit(-1)

    return False

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], '')

    if len(args) == 0:
        msg = 'Too few arguments!'
        usage()
        log(LogLevel.error, msg)
        sys.exit(-1)

    dws_path = os.path.abspath(args[0])
    gen_path = os.path.dirname(dws_path)
    log_path = os.path.dirname(dws_path)
    gen_spec = []

    if len(args) > 1:
        gen_path = os.path.abspath(args[1])
    if len(args) > 2:
        log_path = os.path.abspath(args[2])
    if len(args) > 3:
        gen_spec = args[3:]

    log(LogLevel.info, f'DWS file path is {dws_path}')
    log(LogLevel.info, f'Gen files path is {gen_path}')
    log(LogLevel.info, f'Log files path is {log_path}')

    for item in gen_spec:
        log(LogLevel.info, f'Parameter is {item}')

    if not os.path.exists(dws_path):
        log(LogLevel.error, f'Cannot find "{dws_path}", file not exist!')
        sys.exit(-1)

    if not os.path.exists(gen_path):
        log(LogLevel.error, f'Cannot find "{gen_path}", gen path not exist!')
        sys.exit(-1)

    if not os.path.exists(log_path):
        log(LogLevel.error, f'Cannot find "{log_path}", log path not exist!')
        sys.exit(-1)

    if is_oldDws(dws_path, gen_spec):
        sys.exit(0)

    chipId = ChipObj.get_chipId(dws_path)
    log(LogLevel.info, f'Chip ID: {chipId}')
    chipObj = ChipObj(dws_path, gen_path)

    chip_class_mapping = {
        'MT6797': MT6797,
        'MT6757': MT6757,
        'MT6757-P25': MT6757_P25,
        'MT6570': MT6570,
        'MT6799': MT6799,
        'MT6759': MT6759,
        'MT6763': MT6763,
        'MT6750S': MT6750S,
        'MT6758': MT6758,
        'MT6739': MT6739,
        'MT8695': MT8695,
        'MT8168': MT8695,
        'MT6771': MT6771,
        'MT6775': MT6771,
        'MT6765': MT6771,
        'MT3967': MT6771,
        'MT6761': MT6771,
        'MT6779': MT6779,
        'MT6768': MT6768,
        'MT6785': MT6785,
    }

    if chipId in chip_class_mapping:
        chipObj = chip_class_mapping[chipId](dws_path, gen_path)

    if not chipObj.parse():
        log(LogLevel.error, f'Parse {dws_path} failed!')
        sys.exit(-1)

    if not chipObj.generate(gen_spec):
        log(LogLevel.error, 'Generate files failed!')
        sys.exit(-1)

    sys.exit(0)
