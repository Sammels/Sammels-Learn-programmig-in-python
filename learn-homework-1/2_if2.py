"""

Домашнее задание №1

Условный оператор: Сравнение строк

* Написать функцию, которая принимает на вход две строки
* Проверить, является ли то, что передано функции, строками. 
  Если нет - вернуть 0
* Если строки одинаковые, вернуть 1
* Если строки разные и первая длиннее, вернуть 2
* Если строки разные и вторая строка 'learn', возвращает 3
* Вызвать функцию несколько раз, передавая ей разные праметры 
  и выводя на экран результаты

"""

def main(string1:str, string2:str) -> int:
  if isinstance(string1, str) and isinstance(string2,str):
    if len(string1) == len(string2):
      return 1
    elif len(string1) > len(string2):
      return 2
    elif len(string1.lower()) != len(string2.lower()) and string2 == 'learn':
      return 3
  if not isinstance(string1, str) and not isinstance(string2,str):
    return 0



    
if __name__ == "__main__":
    print(main('один', 'Один'))
    print(main('один', 'два'))
    print(main('один', 'learn'))
    print(main(1,2))
