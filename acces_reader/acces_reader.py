import pyodbc

# Microsoft Access Driver (*.mbd, '
#                          r'*.accdb)

dd = [x for  x in pyodbc.drivers()]
print(dd)



connect = pyodbc.connect(r'Driver={ODBC Driver 18 for SQL Server};DBQ=acces_reader/1.accdb;')
cursor = connect.cursor()
cursor.execute('SHOW TABLES')
for data in cursor.fetchall():
    print(data)
