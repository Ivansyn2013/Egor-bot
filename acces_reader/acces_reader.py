import pyodbc


connect = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mbd, '
                         r'*.accdb)};DBQ=acces_reader/FODMAP DB совсем финал.accdb;')
cursor = connect.cursor()
cursor.execute('SHOW TABLES')
for data in cursor.fetchall():
    print(data)