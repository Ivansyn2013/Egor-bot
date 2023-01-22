

STR_ANSWER_AND_QUESTION = {
    "что такое СРК?":
'''Синдром раздраженного кишечника (СРК) – это хроническое функциональное заболевание кишечника, когда в кишечнике нет значимых патологических изменений, но имеются повышенная чувствительность его стенок, нарушение моторики, что и приводит к возникновению болей и изменению характера стула.

🔸Кишечник с повышенной чувствительностью и моторикой будет реагировать прежде всего на давление изнутри кишечника (например кишечные газы 🫧).

🔸Им страдают порядка 15% от общей популяции! 🌏

🔹Основными симптомами являются:
- боли в животе
- изменения стула (запор или диарея) или его учащение

🔹Боли, чаще схваткообразного/спастического характера различной интенсивности.

🔹Могут усиливаться или возникать:
- перед походом в туалет
- на фоне стресса
- после еды
- в зависимости от менструального цикла

🔹Боли проходят или уменьшаются:
- после похода в туалет
- отхождения кишечных газов

🔹Типичным является изменение характера стула 💩:
- запоры
- диарея
''',
    "как пользоваться ботом?":
'''🔷Под любым продуктом указано, является ли он 🟢low-FODMAP🟢 или 🔴high-FODMAP🔴, в зависимости от содержания FODMAP-веществ.

🟢low-FODMAP🟢 - безопасный продукт, который не должен привести к возникновению симптомов
🔴high-FODMAP🔴 - опасный продукт, от которого наиболее вероятно возникнут симптомы

🔷В боте используется система светофора - 🟢🟡🔴, каждый цвет соответствует уровню опасности.

Пример:
🟢Безопасная доза - 65г (1/3 чашки)

Эта доза является безопасной и, наиболее вероятно, не вызовет симптомов.
Она составляет 65г, что соответствует 1/3 чашки (американская мера: 1 чашка = 237 мл)

Эта доза не является дневным ограничением, она относится к 1 приему пищи, т.е. за день можно съесть ее несколько раз (например на завтрак, обед и ужин)

🔴Опасная доза - 130г (2/3 чашки)

Данная доза наиболее вероятно вызовет неприятные симптомы, такой объем продукта стоит избегать в один прием пищи.

🔷В каждой дозе указаны основные FODMAP вещества:
<code>Фруктоза  🟡 Лактоза   🟢
Маннитол  🟢 Сорбитол  🟢
ГОС       🟢 Фруктаны  🔴</code>

*ГОС - сокращение от ГалактоОлигоСахариды

В данном примере видно, что доза является опасной за счет высокого содержания фруктанов и среднего содержания фруктозы.

❗️При комбинировании различных продуктов, учитывайте, что одни и те же вещества, даже если они имеются в средней дозе 🟡 могут накладываться друг на друга и увеличиваться до опасных объемов 🔴''',
    'кому поможет этот бот?':
'''Этот бот поможет:
✅ Пациентам с синдромом раздраженного кишечника
✅ Пациентам с синдромом избыточного бактериального роста
✅ Пациентам с функциональной диареей
✅ Любому человеку с повышенным газообразованием/метеоризмом
✅ Тем людям, кто хочет понять, от каких продуктов могут возникнуть неприятные симптомы со стороны кишечника
''',
    'что такое low-FODMAP диета?':
'''Low-FODMAP диета (FODMAP – ферментируемые олиго- ди- моносахариды и полиолы)

🔹Это важнейшая часть терапии таких заболеваний, как синдром раздраженного кишечника и синдром избыточного бактериального роста в тонкой кишке.

🔹При соблюдении диеты около 86% пациентов отмечают уменьшение симптомов. 😮

🔹Она заключается в ограничении продуктов 🍎🍑🧅, содержащих углеводы и сахарные спирты. Эти вещества ферментируются бактериями в кишечнике, что приводит к образованию большого количества газов💨 (прежде всего метана и водорода), а еще осмотически удерживают жидкость 💧 в его просвете (за счет "притягивания" ее на себя, в просвет кишечника).

🔹Таким образом, при соблюдении диеты:
- уменьшается объем газов в кишечнике
- уменьшается объем каловых масс за счет жидкости

Это ведет к уменьшению симптомов (например боли и диареи) 😌''',

}

if __name__ == "__main__":
    for q , a in STR_ANSWER_AND_QUESTION.items():
        print(q)
        print(a)