import sys
import re
import math
import random
import string 
from collections import Counter, defaultdict
from _tokenize import Tokenizer
from _models import KneyserNey, WrittenBell

def prepare_testdata(noofsentences, tokens):
    n = len(tokens)-1
    testdata = []
    for i in range(noofsentences):
        idx = random.randint(0, n)
        tempdata = tokens.pop(idx)
        testdata.append(tempdata)
        n-=1
    return testdata, tokens

input_sentence = input("Enter sentence:")
path = sys.argv[2]
smoothing = sys.argv[1]

with open(path, 'r', encoding='utf8') as f:
    corpus = f.read()
    
tokenizer = Tokenizer()
cleaned_corpus = tokenizer._clean_corpus(corpus)
tokens = tokenizer._tokenize(cleaned_corpus)

test_data, tokens = prepare_testdata(1000, tokens)
output_file = '2020201048_LM1_train-perplexity.txt'

if(smoothing == 'k'):
    kneser_ney = KneyserNey(ngrams=4)
    kneser_ney.train(tokens)
    kneser_ney.evaluate(test_data, output_file)
else:
    written_bell = WrittenBell(ngrams = 4)
    written_bell.train(tokens)
    written_bell.evaluate(tokens, output_file) 
 
