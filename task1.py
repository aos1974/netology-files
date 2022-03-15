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
    return True

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

#
# Главная функция программы
#

def main() -> bool:

    # загружаем рецепты из файла
    if not load_cook_book(RECIPES_FILE, cook_book):
        return False
    

    # выводим загруженные рецепты на экран
    print(f'Загружены следующие рецепты из файла {RECIPES_FILE}:')
    print(cook_book)

    return True

#
# Основная программа
#

if main():
    print('Работа программы завершена успешно!')
else:
    print('ERROR: работа программы завершена с ошибкой!')