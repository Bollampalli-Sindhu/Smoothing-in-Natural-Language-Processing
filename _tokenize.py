import sys
import re
import math
import random
import string

class Tokenizer():
    def __init__(self):
        self.words = "[\w']+"
        self.punctuations = ['\.+', '\?+', '\!+', '\:+', '\;+', '\,+', '\-+', "\'+", '\(+','\)+','\[+','\]+','\{+','\}+','\<+','\>+', '\#+']
        self.hashtags = "#[a-zA-Z0-9]+"
        self.mentions = "@[a-zA-Z0-9]+"
        self.urls = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
             
    def _clean_corpus(self, corpus, Remove_punctuations=False):
        corpus1 =  re.sub(self.hashtags,'<HASHTAG>' ,corpus)
        corpus1 =  re.sub(self.mentions,'<MENTION>' ,corpus1)
        corpus1 =  re.sub(self.urls,'<URL>' ,corpus1)
        if Remove_punctuations:
            for i,punct in enumerate(self.punctuations):
                corpus1 = re.sub(punct, '', corpus1)
        else:
            replace_punct = ['.','?', '!', ':', ';', ',', '-', "'", '(', ')', '[', ']', '{', '}', '<', '>', '#']
            for i,punct in enumerate(self.punctuations):
                corpus1 = re.sub(punct, replace_punct[i], corpus1)
            corpus1 = re.sub( r"([a-zA-Z0-9<>])([!,.?;:\-\[\]\{\}\(\)'])", r'\1 \2', corpus1)
            corpus1 = re.sub( r"([!,.?;:\-\[\]\{\}\(\)'])([a-zA-Z0-9<>])", r'\1 \2', corpus1 )
            corpus1 = re.sub( r'([a-zA-Z0-9<>:?!.])(["])', r'\1 \2', corpus1 )
            corpus1 = re.sub( r'(["])([a-zA-Z0-9<>:?!.])', r'\1 \2', corpus1 )
        return corpus1
        
    def _tokenize(self, corpus):
        tokens = []
        
        sentences = [i.strip() for i in corpus.lower().split('\n')]
        for sent in sentences:
            tokens.append(sent.split())
       
        return tokens        


# path = 'general-tweets.txt'
# with open(path, 'r', encoding='utf8') as f:
#     corpus = f.read()
    
# tokenizer = Tokenizer()
# cleaned_corpus = tokenizer._clean_corpus(corpus)
