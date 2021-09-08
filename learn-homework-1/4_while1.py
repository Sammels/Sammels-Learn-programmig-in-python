"""

Домашнее задание №1

Цикл while: hello_user

* Напишите функцию hello_user(), которая с помощью функции input() спрашивает 
  пользователя “Как дела?”, пока он не ответит “Хорошо”
   
"""


def hello_user()-> str:
    """
    Замените pass на ваш код
    """
    while True:
        check_mood = input("Как дела? ")
        if check_mood.lower() == "хорошо":
            print("Славно. Хорошего дня!")
            break

    
if __name__ == "__main__":
    hello_user()
