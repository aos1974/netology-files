from os import listdir

#
# Определение глобальных переменных и констант
#

# имя файла с описанием рецептов
RECIPES_FILE = 'recipes.txt'
# словарь с рецептами
cook_book = {}

#
# Глобальные функции модуля
#

# преобразование строки ингридиента в словарь
def list_from_str(s: str) -> dict:

    lst = s.split('|')
    dct = {}
    # наименование ингрилиента
    dct['ingredient_name'] = str(lst[0]).strip()
    # количество
    dct['quantity'] = int(str(lst[1].strip()))
    # единица изменения
    dct['measure'] = str(lst[2]).strip()

    return dct

# функция загрузки рецептов из файла
# f_name - имя файла для загрузки
# c_book - словарь для загрузки рецептов из файла
def load_cook_book (f_name: str, c_book: dict) -> bool:

    # проверяем наличие файла для загрузки в текущем каталоге
    if f_name not in list(listdir()):
        print(f'ERROR: Файл с рецептами {RECIPES_FILE} не обнаружен!')
        return False
    
    # открываем файл и загружаем рецепты
    with open(f_name, 'r', encoding='UTF-8') as cb_file:
        key = ''
        cnt = 0
        for line in cb_file:
            # убираем лишние пробелы и спецсимволы в начале и конце строки
            line = line.strip()
            # если загружена пустая строка, то это начало нового блока загрузки
            if len(line) == 0:
                key = ''
                cnt = 0
                continue
            # если первая строка в блоке, то это название блюда - ключ словаря
            if len(key) == 0:
                key = line
                continue
            # если загруженная строка - это цифры, то это кол-во ингридиентов в блюде
            if cnt == 0 and line.isdigit():
                cnt = int(line)
                continue
            # заполняем словарь с рецептами
            if cnt > 0:
                if key not in c_book.keys():
                    # если это первый элемент рецепта
                    c_book[key] = []
                # добавляем ингридиент
                c_book[key].append(list_from_str(line))
    # конец загрузки словаря с рецептами

    return True

# функция составления списка закупок на основе заказанных блюд и кол-ва гостей
def get_shop_list_by_dishes(dishes: list, person_count: int) -> dict:

    # список закупок
    shop_list = {}

    # перебираем все блюда в заказе и делаем расчет
    for dish in dishes:
        # пропускаем блюдо если его нет в списке рецептов
        if dish not in cook_book.keys():
            continue
        # состав блюда
        cook_list = list(cook_book.get(dish))
        # выполняем расчет
        for ingredient in cook_list:
            if ingredient['ingredient_name'] in shop_list.keys():
                qt = shop_list[ingredient['ingredient_name']]['quantity']
                qt += ingredient['quantity'] * person_count
                shop_list[ingredient['ingredient_name']]['quantity'] = qt
            else:
                shop_list[ingredient['ingredient_name']] = {'measure': ingredient['measure'], 'quantity': ingredient['quantity'] * person_count}
    # конец расчета

    return shop_list

#
# Главная функция программы
#

def main() -> bool:

    # загружаем рецепты из файла
    if not load_cook_book(RECIPES_FILE, cook_book):
        return False
    

    # выводим загруженные рецепты на экран
    print(f'Загружены следующие рецепты из файла {RECIPES_FILE}:')
    print(list(cook_book.keys()))

    # получаем заказ
    print('Введите заказ или "q" для завершения ввода:')
    order = []
    i = 0
    while True:
        order.append(input('Название блюда (или "q" для завершения): '))
        if order[i] == 'q':
            del order[i]
            break
        else:
            i += 1
    # количество гостей
    person_count = int(input('Введите кол-во гостей: '))

    # выполняем расчет листа закупок для приготовления блюд из заказа
    shop_list = get_shop_list_by_dishes(order, person_count)  

    # вывод результатов расчета  
    print('\nНеобходимы следующие ингридиенты для заказа:\n')
    for ingredient in shop_list:
        print(ingredient, shop_list[ingredient])

    return True

#
# Основная программа
#

if main():
    print('\nРабота программы завершена успешно!')
else:
    print('\nERROR: работа программы завершена с ошибкой!')