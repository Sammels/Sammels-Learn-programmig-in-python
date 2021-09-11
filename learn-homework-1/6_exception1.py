"""

Домашнее задание №1

Исключения: KeyboardInterrupt

* Перепишите функцию hello_user() из задания while1, чтобы она 
  перехватывала KeyboardInterrupt, писала пользователю "Пока!" 
  и завершала работу при помощи оператора break
    
"""

def hello_user()-> str:
    while True:
        try:
            check_mood = input("Как дела? ")
            if check_mood.lower() == "хорошо":
                print("Славно. Хорошего дня!")
                break
                
        except KeyboardInterrupt:
            print("\nПока")
            break

    
if __name__ == "__main__":
    hello_user()
