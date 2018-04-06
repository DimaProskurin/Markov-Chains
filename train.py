import re
import os
import pickle
import argparse
import sys
from collections import defaultdict

r_alphabet = re.compile(u'[а-яА-Яa-zA-Z]+')

parser = argparse.ArgumentParser()
parser.add_argument('--input-dir', type=str, default='stdin', help='Путь к папке с файлами для БД текстов')
parser.add_argument('--model', type=str, help='Путь до файла, в который будет сохраняться частотная модель')
parser.add_argument('--lc', action='store_true', default=False, help='Приводит тексты к нижнему регистру')
args = parser.parse_args()


def gen_lines(file):
    with open(file, 'r') as the_file:
        for line in the_file:
            yield line


def gen_tokens(lines):
    for line in lines:
        if args.lc:
            for token in r_alphabet.findall(line.lower()):
                yield token
        else:
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
if args.input_dir == 'stdin':
    dictionary = make_dictionary(gen_tokens(sys.stdin))
else:
    lst_of_files = os.listdir(args.input_dir)
    for file in lst_of_files:
        tmp_dictionary = make_dictionary(gen_tokens(gen_lines(os.path.join(args.input_dir, file))))
        dictionary = {**dictionary, **tmp_dictionary}

with open(args.model, 'wb') as f:
    pickle.dump(dictionary, f)
