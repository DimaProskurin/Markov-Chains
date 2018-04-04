import re
import os
import pickle
import argparse
from collections import defaultdict

r_alphabet = re.compile(u'[а-яА-Яa-zA-Z]+')

parser = argparse.ArgumentParser()
parser.add_argument('--input-dir', type=str, default='stdin', help='Путь к папке с файлами для БД текстов')
parser.add_argument('--model', type=str, help='Путь до файла, в который будет сохраняться частотная модель')
parser.add_argument('--lc', action='store_true', default=False, help='Приводит тексты к нижнему регистру')

args = vars(parser.parse_args())
input_dir = args['input_dir']
model_dir = args['model']
low_case = args['lc']


def gen_lines(file):
    with open(file, 'r') as the_file:
        for line in the_file:
            if low_case:
                yield line.lower()
            else:
                yield line


def gen_tokens(lines):
    for line in lines:
        for token in r_alphabet.findall(line):
            yield token


def make_dictionary(tokens):
    dictionary = dict()
    lst = list(tokens)
    for i in range(len(lst)-1):
        first_word = lst[i]
        second_word = lst[i+1]
        if first_word not in dictionary:
            dictionary[first_word] = defaultdict(int)
        dictionary[first_word][second_word] += 1
    return dictionary


dictionary = {}
if input_dir == 'stdin':
    # здесь я вынужден ограничить пользователя вводом только одной строки,
    # так как иначе непонятно, когда он закончил ввод своего текста
    line = input()
    if low_case:
        tokens = r_alphabet.findall(line.lower())
    else:
        tokens = r_alphabet.findall(line)

    dictionary = make_dictionary(tokens)
else:
    lst_of_files = os.listdir(input_dir)
    for file in lst_of_files:
        tmp_dictionary = make_dictionary(gen_tokens(gen_lines(os.path.join(input_dir, file))))
        dictionary = {**dictionary, **tmp_dictionary}

with open(model_dir, 'wb') as f:
    pickle.dump(dictionary, f)
