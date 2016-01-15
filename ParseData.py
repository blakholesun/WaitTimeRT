import LoadData as ld
import pandas as pd
import numpy as np

def getNumberDays(dfstart, dfend):
    # get the number of days not including the weekends
    A = [d.date() for d in dfstart]
    B = [d.date() for d in dfend]
    return np.busday_count(A, B)


def toDataFrame(sqlFilename):
    dataDict = ld.loadData(sqlFilename)

    dfDict = {}

    # Make dataframes, drop all duplicates on patientsernum
    # except last, reset index
    for data_name, data in dataDict.items():
        tempDat = pd.DataFrame(data)
        tempDat.columns = map(str.lower, tempDat.columns)
        # change the column names tmake things easier later
        if data_name == 'RFT':
            tempDat.rename(columns={'creationdate': 'enddate'},
                           inplace=True)
        elif data_name == 'CT':
            tempDat.rename(columns={'scheduledstarttime': 'startdate'},
                           inplace=True)
        elif data_name == 'PRES':
            tempDat.rename(columns={'approvedtimestamp': 'startdate'},
                           inplace=True)
        else:
            tempDat.rename(columns={'creationdate': 'startdate'},
                           inplace=True)
        tempDat.drop_duplicates(subset='patientsernum',
                                keep='last', inplace=True)
        tempDat.reset_index(drop=True, inplace=True)
        dfDict[data_name] = tempDat

    # Get the age of each patient at the time of RFT, clean up data
    dfDict['RFT']['dateofbirth'] = (pd.DatetimeIndex(dfDict['RFT']['enddate']).year
                                    - dfDict['RFT']['dateofbirth'])
    dfDict['RFT'].rename(columns={'dateofbirth': 'age'},
                         inplace=True)
    dfDict['RFT']['sex'] = dfDict['RFT']['sex'].str.strip()

    # Merge and create a dictionary of data frames that have wait times
    for data_name, data in dfDict.items():
        if data_name == 'RFT':
            continue
        dfDict[data_name] = pd.merge(dfDict[data_name], dfDict['RFT'],
                                     how='inner', on='patientsernum')
        dfDict[data_name]['timediff'] = getNumberDays(
                dfDict[data_name]['startdate'],
                dfDict[data_name]['enddate'])
        dfDict[data_name] = dfDict[data_name][dfDict[data_name].timediff >= 0]
        dfDict[data_name] = dfDict[data_name][dfDict[data_name].timediff <= 30]
        if data_name == 'CT':
            dfDict[data_name] = dfDict[data_name][dfDict[data_name].prioritycode_x
                                                  == dfDict[data_name].prioritycode_y]
            dfDict[data_name].drop(dfDict[data_name].columns[[0, 2, 3, 4, 5]],
                                   axis=1, inplace=True)
            dfDict['CT'].rename(columns={'prioritycode_y': 'prioritycode'},
                                inplace=True)
        else:
            dfDict[data_name].drop(dfDict[data_name].columns[[0, 1, 3, 4]],
                                   axis=1, inplace=True)

        # Reset the indices just incase.
        dfDict[data_name].reset_index(drop=True, inplace=True)

        # Get dummies to create a sparse matrix and convert into a numpy array
        colsfordummy = ['diagnosiscode', 'doctorsernum',
                        'prioritycode', 'sex']
        tempDat = dfDict[data_name]['age'].values.reshape(
                len(dfDict[data_name]['age'].values), 1)
        for col in colsfordummy:
            tempDat = np.hstack((tempDat,
                                 pd.get_dummies(dfDict[data_name][col]).values))
        tempDat = np.hstack((tempDat, dfDict[data_name]['timediff'].values.reshape(
                len(dfDict[data_name]['timediff'].values), 1)))
        dfDict[data_name] = tempDat

    dfDict.pop('RFT', None)
    print('Data Parsed')
    return dfDict


if __name__ == "__main__":
    sqlfilename = input("Type sql script filename: ")
    dfDict = toDataFrame(sqlfilename)
