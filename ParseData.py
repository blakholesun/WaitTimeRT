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

    #Make dataframes, drop all duplicates on patientsernum
    #except last, reset index    
    for data_name, data in dataDict.items() :
        tempDat = pd.DataFrame(data)
        tempDat.columns = map(str.lower, tempDat.columns)
        tempDat.drop_duplicates(subset = 'patientsernum', 
                                    keep = 'last', inplace = True)
        tempDat.reset_index(drop = True, inplace = True)
        dfDict[data_name] = data

    #Merge and create a dictionary of data frames that have wait times

    for data_name, data in dfDict.items():
        if data_name == 'RFT':
            continue
        dfDict[data_name] = pd.merge(dfDict[data_name], dfDict['RFT'],
                            how = 'inner', on = 'patientsernum')
        dfDict[data_name] = dfDict[data_name][dfDict[data_name].prioritycode_x 
                            == dfDict[data_name].prioritycode_y]


    #for df in dflist:





    #TODO   
    #       Get all the features DIAG, ONC, PRIORITY, AGE, SEX (Binary vector)
    #       Add number of patients in system when created
    #       Add oncologist load
    #       Try with new dataset

    return dfDict

if __name__ == "__main__":
    sqlfilename = input("Type sql script filename: ")
    dfList = toDataFrame(sqlfilename)