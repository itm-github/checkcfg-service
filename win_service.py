#!/usr/bin/python3
# -*- coding: utf-8 -*-

from logging import Formatter, Handler
import logging
import os

import win32serviceutil
import win32service
import win32event
import servicemanager
import sys

import jobs



def _configure_logging():
  
    formatter = Formatter('%(message)s')
    handler = _Handler()
    handler.setFormatter(formatter)
    
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def _main():

    _configure_logging()

    # меняем рабочую папку на текущую, откуда запускается исполняемый файл
    wd = os.path.dirname(sys.argv[0])
    os.chdir(wd)

    # регистрация планировщиков заданий копирования и отчетности
    jobs.reg_jobs()
    
    if len(sys.argv) == 1 and \
            sys.argv[0].endswith('.exe') and \
            not sys.argv[0].endswith(r'win32\PythonService.exe'):
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(checkCfgService)
        servicemanager.StartServiceCtrlDispatcher()
    
    else:

        if len(sys.argv) == 2 and sys.argv[1] == 'help':
            sys.argv = sys.argv[:1]
             
        win32serviceutil.HandleCommandLine(checkCfgService)



class _Handler(Handler):
    def emit(self, record):
        servicemanager.LogInfoMsg(record.getMessage())
        
    
class checkCfgService(win32serviceutil.ServiceFramework):
    
    
    _svc_name_ = 'checkCfgService'
    _svc_display_name_ = 'checkCfgService'
    _svc_description_ = 'checkCfgService'
 
 
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self._stop_event = win32event.CreateEvent(None, 0, 0, None)
 
 
    def GetAcceptedControls(self):
        result = win32serviceutil.ServiceFramework.GetAcceptedControls(self)
        result |= win32service.SERVICE_ACCEPT_PRESHUTDOWN
        return result

    
    def SvcDoRun(self):

        _log('has started')

        while True:

            result = win32event.WaitForSingleObject(self._stop_event, 5000)
              
            if result == win32event.WAIT_OBJECT_0:
                  
                _log('is stopping')
                break

            else:
                # запуск ожидания и выполнения задач
                jobs.run_jobs()
 
        _log('has stopped')
        
        
    def SvcOtherEx(self, control, event_type, data):
             
        if control == win32service.SERVICE_CONTROL_PRESHUTDOWN:
            logging.info('received a pre-shutdown notification')
            self._stop()
        else:
            logging.info('received an event: code={}, type={}, data={}'.format(
                    control, event_type, data))
    

    def _stop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self._stop_event)


    def SvcStop(self):
        self._stop()
    

def _log(fragment):
    message = 'The {} service {}.'.format(checkCfgService._svc_name_, fragment)
    logging.info(message)


if __name__ == '__main__':
    _main()
