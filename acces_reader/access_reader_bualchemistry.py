import sqlalchemy
import sqlalchemy as sql
from sqlalchemy.orm import Session
import chardet
from sqlalchemy.sql import  text

connecting_string = (
    r'DRIVER={MDBTools};'
    r'DBQ=1.accdb;'
    r'charset=utf8;'
    r'ExtendedAnsiSQL=1;'
)

connecting_url = sql.engine.URL.create(
    'access+pyodbc',
    query={'odbc_connect': connecting_string}
)
print (connecting_url)
engine = sql.create_engine(connecting_url)

session = Session(bind=engine)
#
metadata = sqlalchemy.MetaData()
#
# metadata.reflect(engine)
metadata.bind=engine
if metadata.is_bound():
    print("Connetion ok")

#engine.execute('SET NAMES utf8')
#engine.execute('SET character_set_connection=utf8')
# dd = metadata.reflect()
# print (dd)



#tabels = engine.table_names()
#print(tabels)
tabels1 = engine.execute('list tables').fetchall()
for i in tabels1[1:]:
    print(i)
    code = i[0].encode('cp1251').decode('utf8')
    print(code)
    #print(chardet.detect(i))
    #tmp = session.query(text(code)).all()
    #print(tmp)

    data_for_tab = engine.execute(f'SELECT * FROM {code}')
#session.query().union_all()

data_tab1 = engine.execute(f'SELECT * FROM {tabels1[3][0]}')
#

# # for i in data_tab1:
# #     print(i)
# print(metadata.tables.keys())
#
# session = Session(bind=engine)
# dd = ('Доза',)
#
# print(session.query().all())