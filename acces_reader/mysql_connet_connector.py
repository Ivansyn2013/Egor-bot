import logging
import os

from dotenv import load_dotenv
from mysql.connector import connect, Error

load_dotenv()

DEBUG = os.getenv('DEBUG')
BD_PASS = os.getenv('DB_PASS')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
DB_HOST = os.getenv('DB_HOST')


async def db_mysql_request(request: str):
    '''Function connecting to mysql db and return dict with all values for product or None if seach
    result is empty or raise an Error'''

    try:
        with connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=BD_PASS,
                database=MYSQL_DATABASE,
        ) as connection:
            print(connection)
            print("Соединение с базой")
            request = request.replace("\'", '')
            select_req_string = fr'SELECT * FROM Common ' \
                                fr'JOIN dose ON Common.id = dose.common_id ' \
                                fr'JOIN fodmap ON Common.fodmap_id = fodmap.id ' \
                                fr'JOIN Color ON dose.color_id = Color.id ' \
                                fr'LEFT JOIN jpeg_images ON jpeg_images.common_id =' \
                                fr'Common.id ' \
                                fr"WHERE `Название продукта` = '{request}'"

            display_answer = fr'SELECT `Отображение` FROM Color'
            with connection.cursor() as cr:
                cr.execute(select_req_string)
                # это кортеж из табличных строк
                req_all = cr.fetchall()

                if not req_all:
                    return None

                firts_list = [[] for x in range(len(req_all[0]))]
                for y in range(len(req_all)):
                    for x in range(len(req_all[y])):
                        firts_list[x].append(req_all[y][x])
                # return cr.fetchall()
                str_dict = dict(zip(cr.column_names, firts_list))

                cr.execute(display_answer)
                display = cr.fetchall()
                str_dict['Отображение'] = display
                return str_dict

    except Error as e:
        print('Это ошибка', end='')
        print(e)
        return None


async def db_mysql_all_products() -> dict:
    '''dict with all products from db or None if error
        :return: dict or None'''

    request = r'SELECT `id`, `Название продукта` FROM Common'

    #print(BD_PASS)
    #print(DB_HOST)
    try:
        with connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=BD_PASS,
                database=MYSQL_DATABASE
        ) as connection:
            print('Соединение с базой из all_produts')
            logging.info('Соединение с базой из all_produts')
            with connection.cursor() as cr:
                cr.execute(request)
                answer_row = cr.fetchall()

                if answer_row is None:
                    return None
                else:
                    return {x: y for y, x in answer_row}

    except Error as e:
        print('Это ошибка из all+products')
        print(e)
        return None


async def db_mysql_category_request() -> dict:
    """
    connecting with db immutabel request
    :return: dict with category and id of products
    """

    request = fr'SELECT Common.`id`, Category.`Название категории продукта` ' \
              fr'FROM Category, Common ' \
              fr'WHERE Category.`id` = Common.`product_cat_id`'

    answer_dict = {}

    try:
        with connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=BD_PASS,
                database=MYSQL_DATABASE,
        ) as connection:
            print('Соединение с базой из category_products')
            with connection.cursor() as cr:
                cr.execute(request)
                answer_row = cr.fetchall()
                # print(answer_row)
                if answer_row is None:
                    return None
                else:
                    for id, name in answer_row:
                        if name in answer_dict.keys():
                            answer_dict[name].append(id)
                        else:
                            answer_dict[name] = [id]

                    # print(answer_dict)
                    return answer_dict

    except Error as e:
        print('Это ошибка из category_products')
        print(e)
        return None


async def db_mysql_search_product_id(item) -> vars:
    '''

    :param item: product name
    :return : id of product from db
    '''

    request = rf"SELECT id FROM `Common`WHERE `Название продукта` =  '{item}'"
    try:
        with connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=BD_PASS,
                database=MYSQL_DATABASE,
        ) as connection:
            with connection.cursor() as cr:
                cr.execute(request)
                result = cr.fetchone()
        return result[-1]

    except Error as e:
        print('Это ошибка из db_mysql_search_product_id')
        print(e)
        return None


async def db_mysql_update_photo(id, photo):
    '''
    Update photo in DB
    :param id: product id
    :return : None
    '''

    # надо писать запросы через коннектор именно так
    request_update = '''UPDATE jpeg_images SET image = %s WHERE common_id = %s'''
    request_insert = '''INSERT INTO jpeg_images(image, common_id) VALUES (%s, %s)'''
    request_find_record = f'SELECT image FROM jpeg_images WHERE common_id = {id}'
    request_data = (photo, id)

    try:
        with connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=BD_PASS,
                database=MYSQL_DATABASE,
        ) as connection:
            with connection.cursor(buffered=True) as cursor:
                cursor.execute(request_find_record)
                if  cursor.fetchone() is not None:
                    cursor.execute(request_update, request_data)
                else:
                    cursor.execute(request_insert, request_data)

                connection.commit()
                return True

    except Error as e:
        print('Это ошибка из db_mysql_update_photo')
        print(e)
        return False


if __name__ == '__main__':

    def mysql_connector_test(*id):
        '''test func '''
        try:
            with connect(
                    host=DB_HOST,
                    port=DB_PORT,
                    user=DB_USER,
                    password=BD_PASS,
                    database=MYSQL_DATABASE,
            ) as connection:
                print("Соединение с базой")

                select_req_string = fr'SELECT * FROM Common ' \
                                    fr'LEFT JOIN jpeg_images on jpeg_images.common_id' \
                                    fr' = Common.id ' \
                                    fr"WHERE `Название продукта` = 'Молоко'"

                find_record = '''SELECT image FROM jpeg_images
                                 WHERE common_id = (SELECT id FROM Common WHERE 
                                 `Название продукта` = 'Молоко')'''

                with connection.cursor() as cr:
                    if cr.execute(find_record) == None:
                        print(' request None')
                        return None
                   # print(cr.execute(select_req_string))

                    req_all = cr.fetchall()
                    print(cr.column_names)
                    firts_list = [[] for x in range(len(req_all[0]))]
                    for y in range(len(req_all)):
                        for x in range(len(req_all[y])):
                            firts_list[x].append(req_all[y][x])

                    str_dict = dict(zip(cr.column_names, firts_list))
                    print(str_dict)
                    return str_dict

        except Error as e:
            print('Это ошибка ', end='')
            print(e)
            return None


    res = mysql_connector_test()
    #res.pop('Картинка')
    #print(res.items())
    #ph = open('../tmp/tmp.jpg', 'rb')
    #print('\n\n\n\n\n')
    # print(*ph)
