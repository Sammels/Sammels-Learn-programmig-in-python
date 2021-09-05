# Списки

# Задача 1
simple_variable_list = [3, 5, 7, 9, 10.5]
print(simple_variable_list)
simple_variable_list.append("Python")
print(len(simple_variable_list))


# Задача 1.2
print(simple_variable_list[0])
print(simple_variable_list[-1])
print(simple_variable_list[2:5])
print(simple_variable_list.remove("Python"))
# Проверка удаления
print(simple_variable_list)


# Словари

# Задача 1
simple_dict = {"city": "Москва", "temperature": 20}
print(simple_dict["city"])
simple_dict["temperature"] = 15
print (simple_dict)

# Задача 1.2
simple_dict.setdefault("country")
# или
print("country" in simple_dict.keys())

print(simple_dict.get("country", "Россия"))
simple_dict["date"] = "27.05.2019"
print(len(simple_dict))
