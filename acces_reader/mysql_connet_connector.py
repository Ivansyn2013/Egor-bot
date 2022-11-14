import os

from mysql.connector import connect, Error


def db_mysql_request(request: str):
    '''Function connecting to mysql db and return dict with value or None if seach
    result is empty or raise an Error'''

    BD_PASS = os.getenv('BD_PASS')
    # print(BD_PASS)
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
            request = request.replace("\'", '')
            select_req_string = fr'SELECT * FROM Common ' \
                                fr'JOIN dose ON Common.id = dose.common_id ' \
                                fr'JOIN fodmap ON Common.fodmap_id=fodmap.id ' \
                                fr'JOIN Color ON dose.color_id = Color.id ' \
                                fr"WHERE `Название продукта` = '{request}'"
            with connection.cursor() as cr:
                cr.execute(select_req_string)
                req_all = cr.fetchall()
                if not req_all:
                    return None

                firts_list = [[] for x in range(len(req_all[0]))]
                for y in range(len(req_all)):
                    for x in range(len(req_all[y])):
                        firts_list[x].append(req_all[y][x])
                # return cr.fetchall()
                return dict(zip(cr.column_names, firts_list))

    except Error as e:
        print('Это ошибка', end='')
        print(e)
        return None


if __name__ == '__main__':
    res = db_mysql_request('Перловка')
    # print(res)
    print(res.keys())
    print(res['Фруктаны'])
