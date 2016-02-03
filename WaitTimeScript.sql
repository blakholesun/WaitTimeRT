SELECT distinct ap.PatientserNum, a.AliasName, ap.ScheduledStartTime, pr.PriorityCode
FROM Appointment ap 
INNER JOIN Patient p ON ap.PatientSerNum = p.PatientSerNum
INNER JOIN Alias a ON a.AliasSerNum = ap.AliasSerNum
INNER JOIN priority pr ON ap.PatientSerNum = pr.PatientSerNum
WHERE a.AliasName = 'Ct-Sim'
ORDER BY PatientSerNum, ScheduledStartTime;

SELECT a.AliasName, t.PatientSerNum, t.CreationDate
FROM Task t 
INNER JOIN Patient p ON p.PatientSerNum = t.PatientSerNum 
INNER JOIN Alias a ON a.AliasSerNum = t.AliasSerNum
WHERE a.AliasName =	'READY FOR MD CONTOUR'
ORDER BY PatientSerNum, CreationDate;

SELECT a.AliasName, t.PatientSerNum, t.CreationDate
FROM Task t 
INNER JOIN Patient p ON p.PatientSerNum = t.PatientSerNum 
INNER JOIN Alias a ON a.AliasSerNum = t.AliasSerNum
WHERE a.AliasName =	'READY FOR DOSE CALCULATION'
ORDER BY PatientSerNum, CreationDate;

SELECT a.AliasName, d.PatientSerNum, d.ApprovedTimeStamp
FROM Document d 
INNER JOIN Patient p ON d.PatientSerNum = p.PatientSerNum
INNER JOIN Alias a ON a.AliasSerNum = d.AliasSerNum
WHERE a.AliasName =	'PRESCRIPTION APPROVED'
ORDER BY PatientSerNum, ApprovedTimeStamp;

SELECT a.AliasName, t.PatientSerNum, t.CreationDate
FROM Task t 
INNER JOIN Patient p ON p.PatientSerNum = t.PatientSerNum 
INNER JOIN Alias a ON a.AliasSerNum = t.AliasSerNum
WHERE a.AliasName =	'READY FOR PHYSICS QA'
ORDER BY PatientSerNum, CreationDate;

SELECT distinct  t.PatientSerNum, p.DateOfBirth, p.Sex, pd.DoctorSerNum, diag.DiagnosisCode, pr.PriorityCode, a.AliasName, t.CreationDate
FROM Task t 
INNER JOIN Patient p ON p.PatientSerNum = t.PatientSerNum
INNER JOIN Alias a ON a.AliasSerNum = t.AliasSerNum
INNER JOIN diagnosis diag ON t.PatientSerNum = diag.PatientSerNum
INNER JOIN priority pr ON t.PatientSerNum = pr.PatientSerNum
INNER JOIN patientdoctor pd ON t.PatientSerNum = pd.PatientSerNum
WHERE a.AliasName = 'READY FOR TREATMENT' and pd.OncologistFlag = 1
ORDER BY PatientSerNum, CreationDate