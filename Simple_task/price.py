# Функции 

# Задача 2

def format_price(price:int) -> str:
	price=int(abs(price))
	return (f"Цена: {price} руб.")

print(format_price(56.24))
