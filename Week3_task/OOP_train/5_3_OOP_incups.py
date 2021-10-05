# Инкапсюляция - сбор переменных в 1 группу

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


# Тестовый прогон
phone = Product('IPhone 12', 100, stock=5)
print(phone)

phone.sell(1)
print(phone)
        
