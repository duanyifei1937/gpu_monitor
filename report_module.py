#!/data/soft/python3.6/bin/python3.6
from prometheus_client import CollectorRegistry, Gauge, pushadd_to_gateway
import requests
import sys
import socket
import time
import json

def report(job='', metric='', desc='', val='', **labels):
    endpoint = "video:" + socket.gethostname()
    ts = int(time.time())
    
    #######  prometheus  #####
    registry = CollectorRegistry()
    if len(labels) > 0:
      labelname = labels.keys()
      g = Gauge(metric.replace('.','_'), desc,labelnames=labelname, registry=registry)
      lastpush = Gauge('lastpush_'+ metric.replace('.','_'), desc,labelnames=labelname, registry=registry)
      g.labels(**labels).set(val)
      lastpush.labels(**labels).set_to_current_time()
      grouping_key = labels
      pushadd_to_gateway('localhost:9091', job=job, grouping_key=grouping_key, registry=registry)
    else:
      g = Gauge(metric.replace('.','_'), desc, registry=registry)
      g.set_to_current_time()
      g.set(int(val))
      pushadd_to_gateway('localhost:9091', job=job, registry=registry)
    
#    #######  eagles  #####
#    eaglesReqBody = [{
#      "endpoint":       endpoint,
#      "metric":         metric,
#      "timestamp":      ts,
#      "step":           60,
#      "value":          int(val),
#      "counterType":    "GAUGE"
#    }]
#    r = requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(eaglesReqBody), timeout=3)
