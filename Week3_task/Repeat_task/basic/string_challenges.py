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
count_e = word_list.count('е')
count_y = word_list.count('у')
count_o = word_list.count('о')
count_i = word_list.count('и')
count_ie = word_list.count('э')
count_Ib = word_list.count('ы')
print(f'Гласных в {word} равно: {count_a+count_e+count_y+count_o+count_i+count_ie+count_Ib}')


# Вывести количество слов в предложении
sentence = 'Мы приехали в гости'
print(len(sentence.split()))


# Вывести первую букву каждого слова на отдельной строке
sentence = 'Мы приехали в гости'
sent_list = sentence.split()

for word in sent_list:
    print(word[0])


print()
# Вывести усреднённую длину слова в предложении
sentence = 'Мы приехали в гости'
sentence.count('ы')
sent_list = sentence.split()
# for word in sent_list:
#     count = len(word)
#     a = count / len(word)
#     print(a)

# firs_word = sent_list[0]
# snd_word = sent_list[1]
# trd_word = sent_list[2]
# forth_word = sent_list[3]
# word_length = len(firs_word) + len(snd_word) + len(trd_word) + len(forth_word)
# avg_word = word_length // len(sent_list)
# print(avg_word) 