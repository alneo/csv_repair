# -*- coding: utf-8 -*-
import csv
import argparse
import os

""" Исправление файлов CSV
  Такие строки с переводом строк в ячейках (без кавычек)
    65,20100500,1,,,Газель,Мотор,Прокладка,Ремонт общий,Виды ремонта:
    Разбор
    Промывка
    Сборка
    чистка,,,13000,20100501
  Превращаем в такие строки
  65,20100500,1,,,Газель,Мотор,Прокладка,Ремонт общий,Виды ремонта: Разбор Промывка Сборка чистка,,,13000,20100501
  
  Такие строки с переводом строк в ячейках (с кавычками)
    65,20100500,1,,,Газель,Мотор,Прокладка,Ремонт общий,"Виды ремонта:
    Разбор
    Промывка
    Сборка
    чистка",,,13000,20100501
  Превращаем в такие строки - удаляем переводы строк
  65,20100500,1,,,Газель,Мотор,Прокладка,Ремонт общий,"Виды ремонта: Разбор Промывка Сборка чистка",,,13000,20100501
"""

def fix_csv_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Читаем шапку

        # Проверим шапку на дубляж
        if len(header) != len(set(header)):
            raise ValueError(f"Строка шапки содержит повторяющиеся имена полей")

        with open(output_file, 'w', newline='', encoding='utf-8') as fixed_csvfile:
            writer = csv.writer(fixed_csvfile)
            writer.writerow(header)  # Write the header row

            for row in reader:
                # print(f"[{len(header)}][{len(row)}] Строка {row}")
                # Проверем, имеет ли строка такое же количество полей, как и заголовок
                if len(row) != len(header):
                    # Собираем оставшиеся поля, пока не будет достигнуто длина шапки
                    fixed_row = row
                    # print(f"[{len(header)}][{len(fixed_row)}] Строка {fixed_row}")
                    # Собираем через запятую
                    while len(fixed_row) < len(header):
                        try:
                            next_field = next(reader)
                            if len(next_field) == 1:
                                # Возьмем строчку и присоединим к предыдущей
                                fixed_row[-1] = fixed_row[-1] + ' '+next_field[0]
                            else:
                                # Пустые строки не берем
                                if len(next_field) != 0:
                                    # Возьмем первый элемент и присоединим к концу предыдущего
                                    fixed_row[-1] = fixed_row[-1] + ' ' + next_field[0]
                                    # Удалим первый элемент
                                    next_field = next_field[1:]
                                    # Соединим все
                                    fixed_row.extend(next_field)
                        except StopIteration:
                            break
                        # print(f"[{len(header)}][{len(fixed_row)}] Строка {fixed_row}")

                    writer.writerow(fixed_row)  # Запишем фиксированную строку
                else:
                    # Уберем переводы строк в полях (замена на пробел)
                    row = [field.replace('\n',' ') for field in row]
                    # Запишем строчку
                    writer.writerow(row)  # Запишем строку как есть


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fix CSV file')
    parser.add_argument("-if", "--input_file", help='Путь к оригинальному CSV файлу', required=True)
    parser.add_argument("-of", "--output_file", help='Путь к результирующему CSV файлу')

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    if not output_file:
        output_file = os.path.splitext(input_file)[0] + '_output' + os.path.splitext(input_file)[1]

    if os.path.isfile(input_file):
        fix_csv_file(input_file, output_file)
    else:
        print('Указанный файл не найден')
