from datetime import datetime, timedelta
'''
Задание:
1.Напечатайте в консоль даты: вчера, сегодня, 30 дней назад
2.Превратите строку "01/01/25 12:10:03.234567" в объект datetime

'''

# Задача 1
# Дельта времени
dt_delta = timedelta(days=1)
dt_delta_mnth = timedelta(days=30)

# Дата сегодня
dt_now = datetime.now()
# Переведем в читабельный формат
rdbl_dt_now = dt_now.strftime('%d.%m.%Y %H:%M')
print(f'Сегодня: {rdbl_dt_now}')

# Вчера
dt_yestrd = dt_now - dt_delta
# Переведем в читабельный формат
rdbl_dt_yestrd = dt_yestrd.strftime('%d.%m.%Y')
print(f'Вчера было: {rdbl_dt_yestrd}')

# Завтра
dt_tommrw = dt_now - dt_delta_mnth
# Переведем в читабельный формат
rdbl_dt_tommrw = dt_tommrw.strftime('%d.%m.%Y')
print(f'30 дней назад было: {rdbl_dt_tommrw}')


# Задача 2
date_string = "01/01/25 12:10:03.234567"
date_dt = datetime.strptime(date_string, '%m/%y/%d %H:%M:%S.%f')
print(date_dt)
