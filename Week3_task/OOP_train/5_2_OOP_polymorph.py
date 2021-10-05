"""
Предмет имеющий многие формы.
Означает, что у разных объектов одинаковый метод может выполнять разные
действия.

В классе Product мы объявл метод и заставляем его выбрасывать exception на 
случай, если мы забудем его реализовать в классе-наследнике
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


    def get_color(self):
        raise NotImplementedError


    def __repr__(self) -> str:
        return f'<Product name: {self.name}, price: {self.price},\
stock: {self.stock}>'


class Phone(Product):
    def __init__(self, name, price, color, discount=0, stock=0,
                 max_discount=20.0):
        super().__init__(name, price, discount, stock, max_discount)
        self.color = color


    def get_color(self):
        return f'Цвет корпуса {self.color}'


    def __repr__(self):
        return f'<Phone name: {self.name}, price: {self.price}, stock: {self.stock}>'


class Sofa(Product):
    def __init__(self, name, price, color, texture, stock=0,
                 discount=0, max_discount=20):
        super().__init__(name, price, stock, discount, max_discount)
        self.color = color
        self.texture = texture

    def get_color(self):
        return f'Цвет обивки: {self.color}, Тип ткани {self.texture}'


    def __repr__(self):
        return f'<Phone name: {self.name}, price: {self.price}, stock: {self.stock}>'


my_phone = Phone('iPhone', 60000, 'Черный')
print(my_phone.get_color())

sofa1 = Sofa('СуперДупер Диван', 120000.20, 'Бежевый', 'Замша')
print(sofa1.get_color())