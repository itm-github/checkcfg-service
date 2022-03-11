#!/usr/bin/python3
# -*- coding: utf-8 -*-

import schedule
import config as c
import functions


# создание объекта планировщика, в котором будут регистрироваться и запускаться задачи
my_schedule = schedule.Scheduler()


# регистрация задач
def reg_jobs():

    for job in c.CONFIG['jobs']:

        if job['reports_schedule']['every'] == "":
            rj = my_schedule.every()
        else:
            rj = my_schedule.every(int(job['reports_schedule']['every']))
        rj.start_day = job['reports_schedule']['timeunit']
        rj.unit = 'weeks'
        rj.at(job['reports_schedule']['at'])
        rj.do(functions.run_checkcfg)        

# запуск задач
def run_jobs():
    my_schedule.run_pending()
