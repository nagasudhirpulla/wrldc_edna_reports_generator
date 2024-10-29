import pandas as pd
import datetime as dt
from scada_fetcher import fetchPntHistData
from config.appConfig import loadAppConfig

# get application config
appConfig = loadAppConfig()

configExcelPath = "PSP.xlsx"
# configSheets = [("Interregional", 0), ("STATE_gen", 2), ("VOLTTEMP", 2),
#                 ("ONEMINREP_New", 2), ("GENSCHACT", 2), ("WRACE", 2)]

reqDt = dt.datetime.now() - dt.timedelta(days=1)
startDt = dt.datetime(reqDt.year, reqDt.month, reqDt.day)
endDt = startDt + dt.timedelta(hours=23, minutes=59)
sampleFreqSecs = 60

# configSheets = ["volttemp","oneminrep_new","genschact"]
# startDatestr = "25-09-2024 00:00:00"
# startDt = dt.datetime.strptime(startDatestr,"%d-%m-%Y %H:%M:%S")
# endDatestr = "25-09-2024 23:59:00"
# endDt = dt.datetime.strptime(endDatestr,"%d-%m-%Y %H:%M:%S")

# for sht, rowOffset in configSheets:
for row in appConfig['files']:
    sht = row['fileName']
    rowOffset = row['offset']
    destFolder = row['destFolder']
    print(f"{sht} report is being generated")
    # get pnts
    # TODO handle duplicate points in config sheet
    pntsDf = pd.read_excel(configExcelPath, sheet_name=sht)
    pntsDf = pntsDf[["PointId", "Name"]]
    reportDf = pd.DataFrame()
    for itr in range(pntsDf.shape[0]):
        # for itr in range(3):
        pnt = pntsDf.iloc[itr, 0]
        pntName = pntsDf.iloc[itr, 1]
        print('{0} - {1}'.format(itr+1, pnt))
        pntData = fetchPntHistData(pnt, startDt, endDt, 'snap', sampleFreqSecs)
        if len(pntData) > 0:
            pntData = [{pntName: s["dval"], "Timestamp": dt.datetime.strptime(
                s['timestamp'].replace('T', ' '), "%Y-%m-%d %H:%M:%S")} for s in pntData]
            pntDataDf = pd.DataFrame(pntData).set_index("Timestamp")
        else:
            pntDataDf = pd.DataFrame(columns=[pntName])
        reportDf = reportDf.merge(
            pntDataDf, how="outer", left_index=True, right_index=True)
    # dumpFilename = r'reports\{}_{}.xlsx'.format(
    #     sht, dt.datetime.strftime(startDt, "%d_%m_%Y"))
    dumpFilename = r'{0}\{1}_{2}.xlsx'.format(destFolder, 
        sht, dt.datetime.strftime(startDt, "%d_%m_%Y"))
    with pd.ExcelWriter(dumpFilename) as writer:
        reportDf.to_excel(writer, index=True, sheet_name='Sheet1', startrow=rowOffset)
