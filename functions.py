#!/usr/bin/python3
# -*- coding: utf-8 -*-


from logging import Formatter, Handler
import logging
import os
import subprocess
import requests
import config as c
import servicemanager


def _configure_logging():
    formatter = Formatter('%(message)s')
    
    handler = _Handler()
    handler.setFormatter(formatter)
    
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class _Handler(Handler):
    def emit(self, record):
        servicemanager.LogInfoMsg(record.getMessage())


_configure_logging()


def run_checkcfg():

    _log('Service "checkCfgService" start collecting PC configuration')

    out = subprocess.run(

        [
            ".\checkcfg.exe"
        ],

        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    _log('standard output:' + out.stdout)
    _log('error output' + out.stderr)

    report_name = os.environ['COMPUTERNAME'] + ".txt"

    if os.path.exists(report_name):
        os.remove(report_name)
  
    os.rename('checkcfg.dat', report_name)
  
    files = {'file': open(report_name,'rb')}
    values = {"path": "cmdb/{}/".format(c.CONFIG['orgname'])}


    r = requests.post(
        c.CONFIG['http_bot_url'], 
        headers={
            "itm-authentication": f"{c.CONFIG['http_user']}:{c.CONFIG['http_password']}"
        },
        files=files,
        data=values
    )

    _log('status code of file uploading:' + str(r.status_code))

def _log(fragment):
    message = 'The {} service {}.'.format('checkCfgService', fragment)
    logging.info(message)