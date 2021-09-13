from collections import Counter
# Задание 1
# Дан список учеников, нужно посчитать количество повторений каждого имени ученика
# Пример вывода:
# Вася: 1
# Маша: 2
# Петя: 2
print("Задача 1")
students = [
    {'first_name': 'Вася'},
    {'first_name': 'Петя'},
    {'first_name': 'Маша'},
    {'first_name': 'Маша'},
    {'first_name': 'Петя'},
]

name = [ppl['first_name'] for ppl in students]
for key, value in Counter(name).items():
    print(f'{key}: {value}')

print()
# Задание 2
# Дан список учеников, нужно вывести самое часто повторящееся имя
# Пример вывода:
# Самое частое имя среди учеников: Маша
print("Задача 2")
students = [
    {'first_name': 'Вася'},
    {'first_name': 'Петя'},
    {'first_name': 'Маша'},
    {'first_name': 'Маша'},
    {'first_name': 'Оля'},
]

names = [ppl['first_name'] for ppl in students]
names_count = {name:names.count(name) for name in names}
max_count = max(names_count.values())
for name,count in names_count.items():
    if count == max_count:
        print(f'{name} количество повторов {count}')
print()

# Задание 3
# Есть список учеников в нескольких классах, нужно вывести самое частое имя в каждом классе.
# Пример вывода:
# Самое частое имя в классе 1: Вася
# Самое частое имя в классе 2: Маша
print("Задание 3")
school_students = [
    [  # это – первый класс
        {'first_name': 'Вася'},
        {'first_name': 'Вася'},
    ],
    [  # это – второй класс
        {'first_name': 'Маша'},
        {'first_name': 'Маша'},
        {'first_name': 'Оля'},
    ],[  # это – третий класс
        {'first_name': 'Женя'},
        {'first_name': 'Петя'},
        {'first_name': 'Женя'},
        {'first_name': 'Саша'},
    ],
]
# ???
for ppl in school_students:
    names = [x["first_name"] for x in ppl]
    names_count = {name:names.count(name) for name in names}
    max_names_count = max(names_count.values())

    for name, values in names_count.items():
        if values == max_count:
            print(name)
print()
# Задание 4
# Для каждого класса нужно вывести количество девочек и мальчиков в нём.
# Пример вывода:
# Класс 2a: девочки 2, мальчики 0 
# Класс 2б: девочки 0, мальчики 2
print("Задача 4")
school = [
    {'class': '2a', 'students': [{'first_name': 'Маша'}, {'first_name': 'Оля'}]},
    {'class': '2б', 'students': [{'first_name': 'Олег'}, {'first_name': 'Миша'}]},
    {'class': '2в', 'students': [{'first_name': 'Даша'}, {'first_name': 'Олег'}, {'first_name': 'Маша'}]},
]
is_male = {
    'Олег': True,
    'Маша': False,
    'Оля': False,
    'Миша': True,
    'Даша': False,
}
for ppl in school:
    boys_count = 0
    girl_count = 0
    for student in ppl['students']:
        for name in student.values():
            if is_male[name]:
                boys_count += 1
            else:
                girl_count += 1

    print(f"В классе {ppl['class']} {girl_count} девочки и {boys_count} мальчика ")

print()
# Задание 5
# По информации о учениках разных классов нужно найти класс, в котором больше всего девочек и больше всего мальчиков
# Пример вывода:
# Больше всего мальчиков в классе 3c
# Больше всего девочек в классе 2a
print("Задача 5")
school = [
    {'class': '2a', 'students': [{'first_name': 'Маша'}, {'first_name': 'Оля'}]},
    {'class': '3c', 'students': [{'first_name': 'Олег'}, {'first_name': 'Миша'}]},
]
is_male = {
    'Маша': False,
    'Оля': False,
    'Олег': True,
    'Миша': True,
}

clases = {}
for clas in school:
    clases[clas["class"]] = {"boys_count": 0, "girls_count": 0}
    boys_count = 0
    girl_count = 0
    for student in clas['students']:
        for name in student.values():
            if is_male[name]:
                clases[clas["class"]]["boys_count"] += 1
            else:
                clases[clas["class"]]["girls_count"] += 1
clas_with_max_girl = ''
max_boys = 0
max_girls = 0
clas_with_max_boy = ''
for clas in clases.keys():
    if max_boys < clases[clas]['boys_count']:
        max_boys = clases[clas]['boys_count']
        clas_with_max_boy = clas
    if max_girls < clases[clas]['girls_count']:
        max_girls = clases[clas]['girls_count']
        clas_with_max_girl = clas

print(f"Больше всего мальчиков в классе {clas_with_max_boy}")
print(f"Больше всего девочек в классе {clas_with_max_girl}")

