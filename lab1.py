import argparse
import collections
import string
from collections import Counter
import re

def count_all_numbers(text):
    #Подсчитывает все числа в тексте
    numbers = re.findall(r'-?\d+[.,]?\d*', text)
    return len(numbers)

parser = argparse.ArgumentParser(description= '')
parser.add_argument('path', type=str, help='file path')
args = parser.parse_args()
file = open(args.path, "r", encoding='utf-8')
content = file.read()
words = content.split()

#Общее количество символов в файле
print("Количество символов -", len(content))

#Количество символов в файле без учёта пробелов
print("Количество символов без пробелов -", len(content) - content.count(" "))

#Количество слов в файле
print("Количество слов -", len(words))

#Количество предложений в файле
sentences = re.findall(r'["...".!?]+(?!\."...")', content)
sentence_count = len(sentences)
print(f"Количество предложений в файле: {sentence_count}")

#Количество всех чисел в файле
count = count_all_numbers(content)
print(f"Количество чисел: {count}")

#Распределение длин слов (сколько слов длины 1, 2, ...)
words = re.findall(r'\b[а-яёa-z]+\b', content, re.IGNORECASE)
word_lengths = [len(word) for word in words]
length_distribution = Counter(word_lengths)

for length in sorted(length_distribution.keys()):
    count = length_distribution[length]
    percentage = (count / len(words)) * 100
    print(f"Слова длиной {length} символов: {count} шт. ({percentage:.1f}%)")

#Средняя и максимальная длина слова
average_length = sum(word_lengths) / len(words)
max_length = max(word_lengths)
print(f"Средняя длина слова = {int(average_length)}")
print(f"Максимальная длина слова = {max_length}\n")


# Распределение частот букв
# Список допустимых букв (латиница + кириллица)
allowed_letters = string.ascii_lowercase + 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

# Фильтрация только букв
letters_only = [char for char in content if char in allowed_letters]

# Подсчёт частот
letter_counts = collections.Counter(letters_only)

# Сортировка по алфавиту и вывод статистики
for letter in sorted(letter_counts):
    print(f"{letter}: {letter_counts[letter]}")


# Топ 10 самых частых слов без учета предлогов и союзов (и, или, то, это, ...)
stop_words = {
    'и', 'или', 'то', 'это', 'а', 'но', 'как', 'что', 'когда', 'где', 'с', 'в', 'на',
    'по', 'у', 'из', 'от', 'до', 'за', 'для', 'о', 'об', 'при', 'без', 'через',
    'над', 'под', 'между', 'же', 'бы', 'не', 'да', 'ну', 'так', 'его', 'ее', 'их'
}

# Чтение текста
with open(args.path, 'r', encoding='utf-8') as f:
    text = f.read().lower()

# Удаление знаков препинания и разделение на слова
translator = str.maketrans('', '', string.punctuation + '«»—…“”')
clean_text = text.translate(translator)
words = clean_text.split()

# Фильтрация стоп-слов
filtered_words = [word for word in words if word not in stop_words]

# Подсчёт частот
word_counts = collections.Counter(filtered_words)

print("\n Топ 10 самых частых слов:")
for word, count in word_counts.most_common(10):
    print(f"{word}: {count}")


# Топ 10 среди биграмм и триграмм (пара и тройка соседних слов)
# Чтение текста
with open(args.path, 'r', encoding='utf-8') as f:
    text = f.read().lower()

# Удаление знаков препинания и разделение на слова
translator = str.maketrans('', '', string.punctuation + '«»—…“”')
clean_text = text.translate(translator)
words = clean_text.split()

# Формирование биграмм и триграмм
bigrams = zip(words, words[1:])
trigrams = zip(words, words[1:], words[2:])

# Подсчёт частот
bigram_counts = collections.Counter(bigrams)
trigram_counts = collections.Counter(trigrams)

print("\n Топ 10 пар слов:")
for pair, count in bigram_counts.most_common(10):
    print(f"{' '.join(pair)}: {count}")
print("\n Топ 10 троек слов:")
for trio, count in trigram_counts.most_common(10):
    print(f"{' '.join(trio)}: {count}")
