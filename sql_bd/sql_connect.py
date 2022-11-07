import sqlite3 as sq

def sql_start():
    global base, cur
    base = sq.connect('egor_bot.db')
    cur = base.cursor()
    if base:
        print('Data base conncted OK')
    base.cursor('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT, description TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO VALUES (?,?,?)', tuple(data.values()))
        base.commit()