
import pymysql

def loadData(user,pwd):
    connection = pymysql.connect(host='localhost',
                                user=user,
                                password=pwd,
                                db='projectschema',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
        # Read a single record
            sqlscript = "SELECT a.AliasName, ap.PatientserNum, ap.ScheduledStartTime, ap.ScheduledEndTime, ap.Status \
                FROM Appointment ap INNER JOIN Patient p ON ap.PatientSerNum = p.PatientSerNum \
                INNER JOIN Alias a ON a.AliasSerNum = ap.AliasSerNum \
                WHERE a.AliasName = 'Ct-Sim' \
                ORDER BY PatientSerNum, ScheduledStartTime"
            cursor.execute(sqlscript)
            ctdata = cursor.fetchall()
            sqlscript = "SELECT a.AliasName, t.PatientSerNum, t.CreationDate, t.CompletionDate, t.Status \
                FROM Task t INNER JOIN Patient p ON p.PatientSerNum = t.PatientSerNum \
                INNER JOIN Alias a ON a.AliasSerNum = t.AliasSerNum \
                WHERE a.AliasName = 'READY FOR TREATMENT' \
                ORDER BY PatientSerNum, CreationDate"
            cursor.execute(sqlscript)
            RFTData = cursor.fetchall()
    finally:
        connection.close()
    return (ctdata, RFTData)

if __name__ == "__main__":
    user = raw_input("Please enter uname: ")
    pwd = raw_input("Please enter pwd: ")
    CTDATA, RFTDATA = loadData(user,pwd)
    print(CTDATA[0])
    print(RFTDATA[0])
    