import csv
'''
Задание

1. Создайте список словарей:
[
{'name': 'Маша', 'age': 25, 'job': 'Scientist'},
{'name': 'Вася', 'age': 8, 'job': 'Programmer'},
{'name': 'Эдуард', 'age': 48, 'job': 'Big boss'},
]
2.Запишите содержимое списка словарей в файл в формате csv
'''


employer_list = [
            {'name': 'Маша', 'age': 25, 'job': 'Scientist'},
            {'name': 'Вася', 'age': 8, 'job': 'Programmer'},
            {'name': 'Эдуард', 'age': 48, 'job': 'Big boss'},
            {'name': 'Толик', 'age': 25, 'job': 'HR'}
        ]

with open('ppl_in_work.csv', 'w', encoding='utf-8') as f:
    field = ['name', 'age', 'job']
    writer = csv.DictWriter(f, field, delimiter=':')
    writer.writeheader()
    for employer in employer_list:
        writer.writerow(employer)
