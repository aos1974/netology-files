from os import listdir

#
# Определение глобальных переменных и констант
#

# имя результируещего файла
RESULT_FILE = 'result.txt'
# маска файлов для поиска
MASK_FILE = '.txt'

#
# Глобальные функции модуля
#

# функция получения списка файлов для обработки
def get_file_list(mask: str) -> list:

    # получаем список файлов в текущей директории
    file_list = listdir()
    # отфильтровываем ненужные файлы
    f = 0
    while f < len(file_list):
        if file_list[f].find(MASK_FILE) < 0:
            del file_list[f]
        else:
            f += 1

    return file_list

# функция подсчета количества строк в файлах из списка
def get_count_list(file_list: list) -> list:

    cnt_list = []
    # проходим по всем файлам из списка
    for file in file_list:
        cnt = 0
        # открываем файлы и подсчитываем строки
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                cnt += 1
        # кол-во строк файла добавляем в список
        cnt_list.append(cnt)

    return cnt_list

# функция записи результатов в файл
def write_result(file_list: list, count_list: list, file_name: str) -> bool:

    # готовим словарь с ключем - количество строк в файле
    df = dict(zip(count_list, file_list))
    # формируем результирующий файл
    rf = open(file_name, 'w', encoding='utf-8')
    # проходим по всем исходным файлам
    while len(df) > 0:
        with open(df.get(min(df)), 'r', encoding='utf-8') as f:
            # записываем имя исходного файла и кол-во строк
            rf.write(df.get(min(df)) + '\n')
            rf.write(str(min(df)) + '\n')
            # записываем содержимое исходного файла
            for line in f:
                rf.write(line.strip() + '\n')
        # удаляем обработанный файл из словаря
        del (df[min(df)])
    # закываем результирующий файл
    rf.close()

    return True
#
# Главная функция программы
#

def main() -> bool:

    # получаем список файлов для обработки
    file_list = get_file_list(MASK_FILE)

    # подсчитываем кол-во строк в файлах
    count_list = get_count_list(file_list)

    # записываем результирующий файл
    if not write_result(file_list, count_list, RESULT_FILE):
        return False

    return True

#
# Основная программа
#

if main():
    print('\nРабота программы завершена успешно!')
else:
    print('\nERROR: работа программы завершена с ошибкой!')
