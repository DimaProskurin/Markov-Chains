import pickle
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, help='Путь до файла, где лежит частотная модель')
parser.add_argument('--length', type=int, help='Длина генерируемой последовательности')
parser.add_argument('--seed', action='store', default='random_seed', help='Начальное слово')
parser.add_argument('--output', type=str, default='stdout', help='Путь до файла, в который будет записан результат')

args = vars(parser.parse_args())

with open(args['model'], 'rb') as f:
    dictionary = pickle.load(f)

sentence = ""
if args['seed'] == 'random_seed':
    seed = random.choice(list(dictionary.keys()))
else:
    seed = args['seed']

sentence += seed + ' '
args['length'] -= 1

current_word = seed
next_word = ''
next_word_lst = []

while args['length'] > 0:
    for key in list(dictionary[current_word].keys()):
        count = dictionary[current_word][key]
        for i in range(count):
            next_word_lst.append(key)
    next_word = random.choice(next_word_lst)
    next_word_lst.clear()
    sentence += next_word + ' '
    args['length'] -= 1
    current_word = next_word

if (args['output'] == 'stdout'):
    print(sentence)
else:
    with open(args['output'], 'w') as f:
        f.write(sentence)
