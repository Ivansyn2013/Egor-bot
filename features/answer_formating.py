def one_srt_answer(response: dict, inx: int):
    r = response

             #f'{r["Название продукта"][0]}\n' \
             #f'{r["high low medium"][0]}\n\n' \
             #f'Безопасная доза' \
    answer = f'{r["Доза"][inx]} {r["Порция"][inx]}\n' \
             f'Фруктоза {(r["Отображение"][r["Фруктоза"][inx]-1])[0]} ' \
             f'Лактоза  {(r["Отображение"][(r["Лактоза"][inx])-1])[0]} \n' \
             f'Маннитол {(r["Отображение"][(r["Маннитол"][inx])-1])[0]} ' \
             f'Сорбитол {(r["Отображение"][(r["Сорбитол"][inx])-1])[0]}\n' \
             f'ГОС      {(r["Отображение"][(r["ГОС"][inx])-1])[0]} ' \
             f'Фруктаны {(r["Отображение"][(r["Фруктаны"][inx])-1])[0]}\n'
    return answer




def get_answer_str(response: dict):
    ''' get dick form db return str for message'''
    r = response
    dose_str = ['Безопасная доза', 'Средняя доза', 'Высокая доза']

    answer = f'{r["Название продукта"][0]}\n' \
             f'{r["high low medium"][0]}\n\n'
    if r == None:
        return None
    elif 4 > len(r['Доза']) > 0 :
        for inx in range(len(list(r.values())[0])):
            answer = f'{answer}{dose_str[inx]} {one_srt_answer(r,inx)}\n'

        return answer
    else:
        raise Exception(f'Ошибка получения ответа запроса, неправльная длинна: {len(r)}')
        return None
