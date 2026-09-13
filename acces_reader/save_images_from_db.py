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

def _save_image(dir_path, id_x, image):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open (f'{dir_path}/{id_x}.png', 'wb') as file:
        file.write(image)
        file.close()
def get_images_and_save(dir_path):


    try:
        with connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=BD_PASS,
                database=MYSQL_DATABASE,
        ) as connection:
            print('Connecting success')
            execute_str = fr'SELECT `common_id`, `image` from jpeg_images;'
            with connection.cursor(execute_str) as cr:
                cr.execute(execute_str)
                images_list = cr.fetchall()
                return images_list

    except Error as er:
        print(f'Error of base connecting :: {er}')
        return None

if __name__ == "__main__":
    tr = get_images_and_save('dsd')
    for (id_x, image) in tr:
        _save_image('output_1', id_x, image)

    print()