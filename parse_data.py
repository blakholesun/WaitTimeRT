import load_data as ld
import pandas as pd
import numpy as np


def get_number_days(dfstart, dfend):
    # get the number of days not including the weekends
    A = [d.date() for d in dfstart]
    B = [d.date() for d in dfend]
    return np.busday_count(A, B) + 1

def get_patient_queue(dfstart, dfend):
    #TODO find way to get either date range or both into same df
    start_temp = pd.DatetimeIndex(dfstart).date
    end_temp = pd.DatetimeIndex(dfend).date
    dfqueue = []
    for date in start_temp:
        temp = start_temp[start_temp<=date]
        temp = end_temp[end_temp>=date]
        dfqueue.append(len(temp))
    return dfqueue

def parse_data(dataDict):
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
            tempDat.drop_duplicates(subset='patientsernum',
                keep='first', inplace=True)
        elif data_name == 'CT':
            tempDat.rename(columns={'scheduledstarttime': 'startdate'},
                inplace=True)
        elif data_name == 'PRES':
            tempDat.rename(columns={'approvedtimestamp': 'startdate'},
                inplace=True)
        else:
            tempDat.rename(columns={'creationdate': 'startdate'},
                inplace=True)
        if data_name != 'RFT':
            tempDat.drop_duplicates(subset='patientsernum',
                keep='last', inplace=True)
        tempDat.reset_index(drop=True, inplace=True)
        dfDict[data_name] = tempDat

    # Get the age of each patient at the time of RFT, clean up data
    # Need to check the data types
    if dfDict['RFT']['dateofbirth'].dtype == dfDict['RFT']['enddate'].dtype:
        dfDict['RFT']['dateofbirth'] = (pd.DatetimeIndex(dfDict['RFT']['enddate']).year
            - pd.DatetimeIndex(dfDict['RFT']['dateofbirth']).year)
    else:
        dfDict['RFT']['dateofbirth'] = (pd.DatetimeIndex(dfDict['RFT']['enddate']).year
            - dfDict['RFT']['dateofbirth'])   
    dfDict['RFT'].rename(columns={'dateofbirth': 'age'},
        inplace=True)
    dfDict['RFT']['sex'] = dfDict['RFT']['sex'].str.strip()

    # Intersect and create a dictionary of data frames that have wait times
    for data_name, data in dfDict.items():
        if data_name == 'RFT':
            continue
        dfDict[data_name] = pd.merge(dfDict[data_name], 
            dfDict['RFT'], how='inner', on='patientsernum')

        # Get business day count
        dfDict[data_name]['timediff'] = get_number_days(
            dfDict[data_name]['startdate'],
            dfDict[data_name]['enddate'])

        # Remove negative days and anything greater than 30
        dfDict[data_name] = dfDict[data_name][dfDict[data_name].timediff > 0]
        dfDict[data_name] = dfDict[data_name][dfDict[data_name].timediff < 30]

        # Ensure that priority codes match for CT and RFT
        if data_name == 'CT':
            dfDict[data_name] = dfDict[data_name][dfDict[data_name].prioritycode_x
                                                  == dfDict[data_name].prioritycode_y]
            dfDict['CT'].rename(columns={'prioritycode_y': 'prioritycode'},
                inplace=True)

        # Reset the indices just incase.
        dfDict[data_name].reset_index(drop=True, inplace=True)

        # Get the number of patients in queue at time of ct
        # dfDict[data_name]['patientload'] = get_patient_queue(
        #     dfDict[data_name]['startdate'],
        #     dfDict[data_name]['enddate'])

        # Get dummies to create a sparse matrix and convert into a numpy array
        colsfordummy = ['diagnosiscode','doctorsernum','prioritycode','sex']
        tempDat = dfDict[data_name]['age'].values.reshape(
                len(dfDict[data_name]['age'].values), 1)
        for col in colsfordummy:
            tempDat = np.hstack((tempDat,
                pd.get_dummies(dfDict[data_name][col]).values))

        # tempDat = np.hstack((tempDat, 
        #     dfDict[data_name]['patientload'].values.reshape(
        #         len(dfDict[data_name]['patientload'].values), 1)))
        
        tempDat = np.hstack((tempDat, 
            dfDict[data_name]['timediff'].values.reshape(
                len(dfDict[data_name]['timediff'].values), 1)))
        
        dfDict[data_name] = tempDat

    dfDict.pop('RFT', None)
    print('Data Parsed')
    return dfDict


if __name__ == "__main__":
    sqlfilename = input("Type sql script filename: ")
    data = ld.load_data(sqlfilename)
    dfDict = parse_data(data)
