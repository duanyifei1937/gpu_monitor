#!/data/soft/python3.6/bin/python3.6
# -*- coding: utf-8 -*-

import json
import os
from gpu_info import parse_gpu_usage_str
from report_module import report


def service_label():
    return os.popen("docker ps | grep 'kvision-modelapi' | awk '{print $NF}' | awk -F '-' '{print $1}' | awk -F '_' '{print $2}'").read().rstrip("\n")


def ai_report(status, api):
    service = service_label()
    report('ai', api, '1 is healthy', status, **{'service': service})


gpu_info = parse_gpu_usage_str()
gpu_util = gpu_info[0]['usage']
memory = gpu_info[0]['memory']
used_memory = gpu_info[0]['used_memory']
used_memory_precent = used_memory / memory

ai_report(gpu_util, 'ai_gpu_util')
ai_report(used_memory_precent, 'ai_gpu_used_memory_precent')

