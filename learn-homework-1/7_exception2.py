"""

Домашнее задание №1

Исключения: приведение типов

* Перепишите функцию discounted(price, discount, max_discount=20)
  из урока про функции так, чтобы она перехватывала исключения,
  когда переданы некорректные аргументы.
* Первые два нужно приводить к вещественному числу при помощи float(),
  а третий - к целому при помощи int() и перехватывать исключения
  ValueError и TypeError, если приведение типов не сработало.
    
"""

def discounted(price:float, discount:float, max_discount:int=20) -> str:
    """
    Замените pass на ваш код
    """
    try:
      price = float(price)
      discount = float(discount)
      max_discount = int(max_discount)
            
      if discount >= 100:
          price_with_discount = price
      else:
          price_with_discount = price - (price * discount / 100)
      return price_with_discount
    except (ValueError,TypeError):
      print ("Приведение типов не сработало")

    
if __name__ == "__main__":
    print(discounted(100, 2))
    print(discounted(100, "3"))
    print(discounted("100", "4.5"))
    print(discounted("five", 5))
    print(discounted("сто", "десять"))
    print(discounted(100.0, 5, "10"))
