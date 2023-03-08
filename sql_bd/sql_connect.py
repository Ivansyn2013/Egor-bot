import sqlite3 as sq

from create_obj import bot


def sql_start():
    global base, cur
    base = sq.connect('egor_bot.db')
    cur = base.cursor()
    #cur.execute('DROP TABLE menu')
    if base:
        print('Data base connected OK')
    cur.execute('CREATE TABLE IF NOT EXISTS menu'
                '(img TEXT, '
                'name TEXT, '
                'description TEXT,'
                'price TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?,?,?,?)', tuple(data.values()))
        base.commit()


#функция чтения из бд и сразу в отправку
async def sql_read(message):
    for data in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(message.from_user.id, data[0], f'{data[1]}\nОписание: '
                                                            f'{data[2]}\n '
                                                            f'Price:{data[3]}')
