import pickle
import random
import argparse
import numpy
import sys

if __name__ == "__main__":
    '''Парсер аргументов консоли'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str,
                        help='Путь до файла, где лежит частотная модель')
    parser.add_argument('--length', type=int,
                        help='Длина генерируемой последовательности')
    parser.add_argument('--seed', action='store', default='random_seed',
                        help='Начальное слово')
    parser.add_argument('--output', type=str, default=None,
                        help='Путь до файла, где будет записан результат')
    args = parser.parse_args()

    '''Загружаем частотную модель'''
    with open(args.model, 'rb') as f:
        dictionary = pickle.load(f)

    '''Открываем файл для записи результата(опционально)'''
    if args.output is not None:
        sys.stdout = open(args.output, 'w')

    '''Выбор начального слова, генерируемой последовательности'''
    if args.seed == 'random_seed':
        seed = random.choice(list(dictionary.keys()))
    else:
        seed = args.seed

    print(seed, end=' ')
    args.length -= 1

    current_word = seed
    next_word = ''

    '''Создание и вывод генерируемой последовательности'''
    for i in range(args.length):
        s = sum(dictionary[current_word].values())
        probability = [item / s for item in dictionary[current_word].values()]

        next_word = numpy.random.choice(
            list(dictionary[current_word].keys()),
            p=probability)
        print(next_word, end=' ')
        current_word = next_word
