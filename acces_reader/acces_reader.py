import pyodbc

# Microsoft Access Driver (*.mbd, '
#                          r'*.accdb)

dd = [x for  x in pyodbc.drivers()]
print(dd)



connect = pyodbc.connect(r'Driver={MDBTools};DBQ=1.accdb;')
cursor = connect.cursor()
cursor.execute('list tables')
for data in cursor.fetchall():
    print(data)
