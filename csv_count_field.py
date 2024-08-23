# -*- coding: utf-8 -*-
import csv
import argparse
import os

def csv_count_field(input_file):
    with open(input_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Читаем шапку

        # Проверим шапку на дубляж
        if len(header) != len(set(header)):
            raise ValueError(f"Строка шапки содержит повторяющиеся имена полей")

        for row in reader:
            if len(row) != len(header):
                print(f"Строка {reader.line_num}: {len(header)}!={len(row)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Count field CSV file')
    parser.add_argument("-if", "--input_file", help='Путь к оригинальному CSV файлу', required=True)

    args = parser.parse_args()

    input_file = args.input_file

    if os.path.isfile(input_file):
        csv_count_field(input_file)
    else:
        print('Указанный файл не найден')
