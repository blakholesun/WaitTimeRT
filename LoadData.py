
import pymysql
import getpass

def loadData(sqlfilename):
    user = input("Please enter uname: ")
    pwd = getpass.getpass('Please enter pwd: ')
    connection = pymysql.connect(host='localhost',
                                user=user,
                                password=pwd,
                                db='projectschema',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Open and read the file as a single buffer
            fd = open(sqlfilename, 'r')
            sqlFile = fd.read()
            fd.close()

            # all SQL commands (split on ';')
            sqlFile = sqlFile.replace('\n', ' ')
            sqlCommands = sqlFile.split(';')
            print(sqlCommands[0])
            dataList = []
            # Execute every command from the input file
            for command in sqlCommands:
                cursor.execute(command)
                dataList.append(cursor.fetchall())
    finally:
        connection.close()
    return dataList

if __name__ == "__main__":
    sqlfilename = input("Type sql script filename: ")
    data = loadData(sqlfilename)