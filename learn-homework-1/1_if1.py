"""

Домашнее задание №1

Условный оператор: Возраст

* Попросить пользователя ввести возраст при помощи input и положить 
  результат в переменную
* Написать функцию, которая по возрасту определит, чем должен заниматься пользователь: 
  учиться в детском саду, школе, ВУЗе или работать
* Вызвать функцию, передав ей возраст пользователя и положить результат 
  работы функции в переменную
* Вывести содержимое переменной на экран

"""

def main():
    """
    Эта функция вызывается автоматически при запуске скрипта в консоли
    В ней надо заменить pass на ваш код
    """
    age = int(input("Добрый день! Введи пожалуйста свой возраст: "))

    if age <= 5:
      print("Добро пожаловать в детский сад")
    elif 6 <= age <= 17:
      print ("Двери школы открыты для Вас")
    elif 18<= age <= 21 or age <= 22:
      print ("Вуз, счастливая пора")
    else:
      print ("Работа не ждет")


if __name__ == "__main__":
    main()
