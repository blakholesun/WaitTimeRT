import pymysql
import getpass


def load_data(sqlfilename):
    user = input("Please enter uname: ")
    pwd = getpass.getpass('Please enter pwd: ')
    print('Please Wait: Querying Database')
    connection = pymysql.connect(host='localhost',
                                 user=user,
                                 password=pwd,
                                 db='projectschema',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    data_names = ['CT', 'MD', 'DOSE', 'PRES', 'PHYS', 'RFT']

    cursor = connection.cursor()
    # Open and read the file as a single buffer
    fd = open(sqlfilename, 'r')
    sqlfile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlfile = sqlfile.replace('\n', ' ')
    sqlcommands = sqlfile.split(';')
    dataList = []
    # Execute every command from the input file
    for index, command in enumerate(sqlcommands):
        cursor.execute(command)
        dataList.append(cursor.fetchall())
        print('Done ', data_names[index])

    connection.close()

    dataDict = dict(zip(data_names, dataList))
    print('SQL query completed. Data Loaded')
    return dataDict


if __name__ == "__main__":
    sqlfilename = input("Type sql script filename: ")
    data = load_data(sqlfilename)
