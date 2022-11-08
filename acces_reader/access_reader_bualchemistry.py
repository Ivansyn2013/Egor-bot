import sqlalchemy as sql
connecting_string = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\Users\Александр\PycharmProjects\Egor-bot\acces_reader\FODMAP DB совсем '
    r'финал.accdb'
    r'ExtendedAnsiSQL=1;'
)

connecting_url = sql.engine.URL.create(
    'access+pyodbc',
    query={'odbc_connect': connecting_string}
)

engine = sql.create_engine(connecting_url)

dd = engine.connect()
print(dd)

