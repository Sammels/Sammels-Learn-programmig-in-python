"""

Домашнее задание №1

Исключения: KeyboardInterrupt

* Перепишите функцию hello_user() из задания while1, чтобы она 
  перехватывала KeyboardInterrupt, писала пользователю "Пока!" 
  и завершала работу при помощи оператора break
    
"""

def hello_user()-> str:
    """
    Замените pass на ваш код
    """
    
    while True:
        try:
            check_mood = input("Как дела? ")
            if check_mood == "Хорошо" or check_mood == "хорошо":
                print("Славно. Хорошего дня!")
                break
                
        except KeyboardInterrupt:
            print("\nПока")
            break

    
if __name__ == "__main__":
    hello_user()
