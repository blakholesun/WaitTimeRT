import LoadData as ld
import pandas as pd

def getNumberDays(start, end):
    # get the number of days not including the weekends

def toDataFrame(sqlFilename):
    dataDict = ld.loadData(sqlFilename)
    print("Data Loaded")
    
    dfDict = []

    for data_name, data in dataDict.items() :
        tempDat = pd.DataFrame(data)
        tempDat.columns = map(str.lower, tempDat.coulmns)
        if data_name == 'RFT' or data_name == 'CT'
            tempDat.drop_duplicates(subset = 'patientsernum', 
                                    keep = 'last', inplace = True)
            tempDat.reset_index(drop = True, inplace = True)

        dfList = dfList.append(tempDat)


    #TODO   Remove weekends (Create new method)
    #       Get all the features DIAG, ONC, PRIORITY, AGE, SEX
    #       Add patient load in system when created
    #       Add oncologist load
    #       Try with new dataset

    return (feature, output)