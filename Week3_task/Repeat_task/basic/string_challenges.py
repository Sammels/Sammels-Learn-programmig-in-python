# Вывести последнюю букву в слове
word = 'Архангельск'
print(word[-1])


# Вывести количество букв "а" в слове
word = 'Архангельск'
word_list = list(word.lower())
count = word_list.count('а')
print(f'А в {word} равно: {count}')

# Вывести количество гласных букв в слове
word = 'Архангельск'
word_list = list(word.lower())
count_a = word_list.count('а')
count_b = word_list.count('е')
print(f'Гласных в {word} равно: {count_a + count_b}')


# Вывести количество слов в предложении
sentence = 'Мы приехали в гости'
print(len(sentence.split()))


# Вывести первую букву каждого слова на отдельной строке
sentence = 'Мы приехали в гости'
sent_list = sentence.split()
firs_word = sent_list[0][0]
snd_word = sent_list[1][0]
trd_word = sent_list[2][0]
forth_word = sent_list[3][0]
print('\n' ,firs_word,'\n',snd_word, '\n', trd_word, '\n',forth_word)


# Вывести усреднённую длину слова в предложении
sentence = 'Мы приехали в гости'
sent_list = sentence.split()
firs_word = sent_list[0]
snd_word = sent_list[1]
trd_word = sent_list[2]
forth_word = sent_list[3]
word_length = len(firs_word) + len(snd_word) + len(trd_word) + len(forth_word)
avg_word = word_length // len(sent_list)
print(avg_word) 