# Наследование

"""
Позволяет общий функционал в класс-родитель, в в производных классах делать,
что отличает от родителя.

Из наследника можно получить доступ к ориг. методам класса-родителя через
через вызов super()

Наследование позволяет вносить общего "Родителя", и в дочерних классах 
определять только тот функционал, который нужен.
"""

class Product:
    def __init__(self,name,price,discount=0,stock=0,max_discount=20.0):
        self.name = name.strip()
        if not len(self.name) >= 2:
            raise ValueError('Слишком короткое название товара')
        
        self.price = abs(float(price))

        self.max_discount = abs(int(max_discount))
        if self.max_discount > 99:
            raise ValueError('Слишком большая скидка')

        self.discount = abs(float(discount))
        if self.discount > self.max_discount:
            self.discount = self.max_discount        
        self.stock = abs(int(stock))


    def sell(self,items_count:int=1) -> int:
        if items_count > self.stock:
            raise ValueError('Недостаточно товара на складе')
        self.stock -= items_count


    def discounted(self) -> float:
        return self.price - (self.price*self.discount/100)


    def __repr__(self) -> str:
        return f'<Product name: {self.name}, price: {self.price},\
stock: {self.stock}>'



class Phone(Product):
    def __init__(self, name, price, color, discount=0, stock=0,
                 max_discount=20.0):
        super().__init__(name, price, discount, stock, max_discount)
        self.color = color


    def __repr__(self):
        return f'<Phone name: {self.name}, price: {self.price}, stock: {self.stock}>'


class Sofa(Product):
    def __init__(self, name, price, color, texture, stock=0,
                 discount=0, max_discount=20):
        super().__init__(name, price, stock, discount, max_discount)
        self.color = color
        self.txture = texture

    def __repr__(self):
        return f'<Phone name: {self.name}, price: {self.price}, stock: {self.stock}>'


phone = Phone('iPhone Xs', 100, 'серый')
print(phone)
print(phone.color)

sofa1 = Sofa('Большой диван', 10, 'Желтый', 'Велюр')
print(sofa1)