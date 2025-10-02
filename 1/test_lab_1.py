import argparse
import string
from collections import Counter
import re

# Количество символов (с учетом пробелов и без)
def count_characters(content):
    total_chars = len(content)
    chars_no_spaces = len(content) - content.count(" ")
    return total_chars, chars_no_spaces

# Количество слов
def count_words(content):
    words = content.split()
    return len(words)

# Количество предложений
def count_sentences(content):
    sentences = re.findall(r'["...".!?]+(?!\."...")', content)
    return len(sentences)

# Количество чисел
def count_all_numbers(text):
    numbers = re.findall(r'-?\d+[.,]?\d*', text)
    return len(numbers)

# Распределение длин слов (сколько слов длины 1, 2, ...)
# Средняя и максимальная длина слова
def analyze_word_lengths(content):
    words = re.findall(r'\b[а-яёa-z]+\b', content, re.IGNORECASE)
    word_lengths = [len(word) for word in words]
    length_distribution = Counter(word_lengths)
    
    average_length = sum(word_lengths) / len(words) if words else 0
    max_length = max(word_lengths) if words else 0
    
    return length_distribution, average_length, max_length

# Распределение частот букв
def analyze_letter_frequency(content):
    allowed_letters = string.ascii_lowercase + 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    
    # Фильтрация только букв
    letters_only = [char.lower() for char in content if char.lower() in allowed_letters]
    
    # Подсчёт частот
    letter_counts = Counter(letters_only)
    
    return letter_counts

def print_word_length_distribution(length_distribution):
    #Выводит распределение длин слов
    for length in sorted(length_distribution.keys()):
        count = length_distribution[length]
        print(f"Слова длиной {length} символов: {count} шт.")

def print_letter_frequency(letter_counts):
    #Выводит частоту букв
    for letter in sorted(letter_counts):
        print(f"{letter}: {letter_counts[letter]}")

# Топ 10 самых частых слов без учета предлогов и союзов
def analyze_top_words(content):
    stop_words = {
        'и', 'или', 'то', 'это', 'а', 'но', 'как', 'что', 'когда', 'где', 'с', 'в', 'на',
        'по', 'у', 'из', 'от', 'до', 'за', 'для', 'о', 'об', 'при', 'без', 'через',
        'над', 'под', 'между', 'же', 'бы', 'не', 'да', 'ну', 'так', 'его', 'ее', 'их'
    }
    
    # Удаление знаков препинания и разделение на слова
    translator = str.maketrans('', '', string.punctuation + '«»—…""')
    clean_text = content.lower().translate(translator)
    words = clean_text.split()
    
    # Фильтрация стоп-слов
    filtered_words = [word for word in words if word not in stop_words]
    
    # Подсчёт частот
    word_counts = Counter(filtered_words)
    
    return word_counts

# Топ 10 среди биграмм и триграмм (пара и тройка соседних слов)
def analyze_ngrams(content):
    # Удаление знаков препинания и разделение на слова
    translator = str.maketrans('', '', string.punctuation + '«»—…""')
    clean_text = content.lower().translate(translator)
    words = clean_text.split()
    
    # Формирование биграмм и триграмм
    bigrams = zip(words, words[1:])
    trigrams = zip(words, words[1:], words[2:])
    
    # Подсчёт частот
    bigram_counts = Counter(bigrams)
    trigram_counts = Counter(trigrams)
    
    return bigram_counts, trigram_counts

def print_top_words(word_counts):
    #Выводит топ 10 самых частых слов
    print("\nТоп 10 самых частых слов:")
    for word, count in word_counts.most_common(10):
        print(f"{word}: {count}")

def print_ngrams(bigram_counts, trigram_counts):
    #Выводит топ 10 биграмм и триграмм
    print("\nТоп 10 пар слов:")
    for pair, count in bigram_counts.most_common(10):
        print(f"{' '.join(pair)}: {count}")
    
    print("\nТоп 10 троек слов:")
    for trio, count in trigram_counts.most_common(10):
        print(f"{' '.join(trio)}: {count}")

def main():
    parser = argparse.ArgumentParser(description='Анализ текстового файла')
    parser.add_argument('path', type=str, help='file path')
    args = parser.parse_args()
    
    try:
        with open(args.path, "r", encoding='utf-8') as file:
            content = file.read()
        
        # Анализ символов
        total_chars, chars_no_spaces = count_characters(content)
        print("Количество символов -", total_chars)
        print("Количество символов без пробелов -", chars_no_spaces)
        
        # Анализ слов
        word_count = count_words(content)
        print("Количество слов -", word_count)
        
        # Анализ предложений
        sentence_count = count_sentences(content)
        print(f"Количество предложений в файле: {sentence_count}")
        
        # Анализ чисел
        number_count = count_all_numbers(content)
        print(f"Количество чисел: {number_count}")
        
        # Анализ длин слов
        length_distribution, average_length, max_length = analyze_word_lengths(content)
        print_word_length_distribution(length_distribution)
        print(f"Средняя длина слова = {int(average_length)}")
        print(f"Максимальная длина слова = {max_length}")
        
        # Анализ частоты букв
        letter_counts = analyze_letter_frequency(content)
        print_letter_frequency(letter_counts)
        
        # Анализ топ слов
        word_counts = analyze_top_words(content)
        print_top_words(word_counts)
        
        # Анализ N-грамм
        bigram_counts, trigram_counts = analyze_ngrams(content)
        print_ngrams(bigram_counts, trigram_counts)
        
    except FileNotFoundError:
        print(f"Ошибка: Файл '{args.path}' не найден")
    except Exception as e:
        print(f"Произошла ошибка при обработке файла: {e}")

if __name__ == "__main__":
    main()