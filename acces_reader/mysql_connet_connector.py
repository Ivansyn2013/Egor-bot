from mysql.connector import connect, Error
import os


def db_mysql_request(request):
    BD_PASS = os.getenv('BD_PASS')
    #print(BD_PASS)
    try:
        with connect(
            host='192.168.0.110',
            port=3300,
            user='test',
            password=BD_PASS,
            database='egor_db'
        ) as connection:
            print(connection)
            print("Соединение с базой")
            request = request.replace("\'",'')
            select_req_string = fr'SELECT * FROM Common ' \
                                fr'JOIN dose ON Common.id = dose.common_id ' \
                                fr'JOIN fodmap ON Common.fodmap_id=fodmap.id ' \
                                fr'JOIN Color ON dose.color_id = Color.id ' \
                                fr"WHERE `Название продукта` = '{request}'"
            with connection.cursor() as cr:
                cr.execute(select_req_string)
                return cr.fetchall()

    except Error as e:
        print('Это ошибка', end='')
        print(e)
        return None


if __name__=='__main__':
    res = db_mysql_request('Перловка')
    print(res)