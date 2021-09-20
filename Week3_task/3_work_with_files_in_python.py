'''
Задание

1. Скачайте файл
2. Прочитайте содержимое файла в переменную, подсчитайте длину получившейся
строки
3. Подсчитайте количество слов в тексте
4. Замените точки в тексте на восклицательные знаки
5. Сохраните результат в файл referat2.txt
'''
# Думаю, как посчитать слова в тексте.......

def read_file() -> str:
    '''
    Функция открывает файл для чтения.
    '''
    with open('referat.txt', 'r', encoding='utf-8') as f:
        text_file = f.read()
        # Длина слов в тексте
        print(f'\nОбщая длинна слов: {len(text_file)}')
        return text_file


def write_file() -> str:
    '''
    Функция создает новый файл referat2.txt.
    Берет текст из функции read_file и заменяет . на !
    '''
    with open('referat2.txt', 'w', encoding='utf-8') as wrt_file:
        wrt_file.write(read_file().replace('.', '!'))


if __name__ == "__main__":
    read_file()
    write_file()
