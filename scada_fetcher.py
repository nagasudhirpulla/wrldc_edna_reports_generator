# -*- coding: utf-8 -*-
import requests
import json
import datetime as dt
from config.appConfig import getAppConfig


def fetchPntHistData(pnt:str, startTime:dt.datetime, endTime:dt.datetime, fetchStrategy:str='snap', secs:int=60):
    appConf = getAppConfig()
    apiBaseUrl = appConf["histApiBaseUrl"]
    startTimeStr = startTime.strftime('%d/%m/%Y/%H:%M:%S')
    endTimeStr = endTime.strftime('%d/%m/%Y/%H:%M:%S')
    params = dict(
        pnt=pnt,
        strtime=startTimeStr,
        endtime=endTimeStr,
        secs=secs,
        type=fetchStrategy
    )
    r = requests.get(url=apiBaseUrl, params=params)
    data = json.loads(r.text)
    return data
