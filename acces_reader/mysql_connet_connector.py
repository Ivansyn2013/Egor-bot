import os

from mysql.connector import connect, Error
from dotenv import load_dotenv



def db_mysql_request(request: str):
    '''Function connecting to mysql db and return dict with value or None if seach
    result is empty or raise an Error'''

    load_dotenv()
    DEBUG = os.getenv('DEBUG')

    if DEBUG:
        DB_HOST = '192.168.0.202'

    BD_PASS = os.getenv('BD_PASS')
    # print(BD_PASS)
    try:
        with connect(
                host=DB_HOST,
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
                                fr'JOIN fodmap ON Common.fodmap_id = fodmap.id ' \
                                fr'JOIN Color ON dose.color_id = Color.id ' \
                                fr'JOIN jpeg_images ON jpeg_images.common_id =' \
                                fr'Common.id ' \
                                fr"WHERE `Название продукта` = '{request}'"

            display_answer = fr'SELECT `Отображение`FROM Color'
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
    request = r'SELECT `id`, `Название продукта` FROM Common'
    load_dotenv()
    DEBUG = os.getenv('DEBUG')
    if DEBUG:
        DB_HOST = '192.168.0.202'

    BD_PASS = os.getenv('BD_PASS')


    try:
        with connect(
                host=DB_HOST,
                port=3300,
                user='test',
                password=BD_PASS,
                database='egor_db'
        ) as connection:
            print('Соединение с базой из all_produts')
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
    BD_PASS = os.getenv('BD_PASS')
    answer_dict = {}
    load_dotenv()
    DEBUG = os.getenv('DEBUG')
    if DEBUG:
        DB_HOST = '192.168.0.202'

    try:
        with connect(
                host=DB_HOST,
                port=3300,
                user='test',
                password=BD_PASS,
                database='egor_db'
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


if __name__ == '__main__':
    res = db_mysql_request('Перловка')
    # print(res)
    # print(res.keys())
    # print(res['Отображение'])

    res.pop('image')
    res.pop('Картинка')
    print(res.items())
    # image_data = res['image'][0]
    # print(len(image_data))
    # print(type(image_data))
    # image = Image.open(io.BytesIO(image_data))
    # image.show()
    # with open('tmp2.jpg', 'wb') as f:
    #     f.save(image_data)
    # print(res["Отображение"][res["Фруктаны"]])
    # print(res["Отображение"][res["Фруктаны"][1]])
    # print(res["Отображение"][res["Фруктаны"][2]])

    # for inx in range(len(list(res.values())[0])):
    #     print('*'*100)
    #     print(f'индекс{inx}')
    #     print(one_srt_answer(res,inx))
    print(db_mysql_all_products())
    res = db_mysql_all_products()
    print(list(res.keys()))
