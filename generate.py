import pickle
import random
import argparse
import numpy
import sys

if __name__ == "__main__":
    MAX_WORDS_IN_SENTENCE = 10

    '''Парсер аргументов консоли'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str,
                        help='Путь до файла, где лежит частотная модель',
                        required=True)
    parser.add_argument('--length', type=int,
                        help='Длина генерируемой последовательности',
                        required=True)
    parser.add_argument('--seed', action='store', default='random_seed',
                        help='Начальное слово')
    parser.add_argument('--output', type=str, default=None,
                        help='Путь до файла, где будет записан результат')
    args = parser.parse_args()

    '''Загружаем частотную модель'''
    with open(args.model, 'rb') as f:
        dictionary = pickle.load(f)
        for word in dictionary:
            amount = sum(dictionary[word].values())
            for second_word in dictionary[word]:
                dictionary[word][second_word] /= amount

    '''Открываем файл для записи результата(опционально)'''
    if args.output is not None:
        sys.stdout = open(args.output, 'w')

    '''Выбор начального слова, генерируемой последовательности'''
    if args.seed == 'random_seed':
        seed = random.choice(list(dictionary.keys()))
    else:
        seed = args.seed

    if seed not in dictionary.keys():
        print('Error! Первое слово отсутствует в словаре.')
    else:
        sentence = [seed]
        args.length -= 1

        current_word = seed
        next_word = ''

        '''Создание и вывод генерируемой последовательности'''
        for i in range(args.length):
            if current_word not in dictionary:
                current_word = random.choice(list(dictionary))

            probability = list(dictionary[current_word].values())

            next_word = numpy.random.choice(
                list(dictionary[current_word].keys()),
                1,
                p=probability)[0]
            sentence.append(next_word)
            if len(sentence) >= MAX_WORDS_IN_SENTENCE:
                print(' '.join(sentence))
                sentence.clear()

            current_word = next_word

        print(' '.join(sentence))
