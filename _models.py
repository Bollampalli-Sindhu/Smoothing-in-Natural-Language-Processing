import sys
import re
import math
import random
import string 
from collections import Counter, defaultdict


class KneyserNey():
    def __init__(self, ngrams=4):
        self.n = ngrams
        
    def train(self, tokens):
        self.ngrams = [0]
        for i in range(1,self.n+1):
            ngrams = get_ngrams(tokens,i)
            self.ngrams.append(ngrams)
    
    def get_words_succeeding_input(self, ngrams, input1, n):
        dic={}
        for key,value in ngrams.items():
            if(key[:n-1] == input1 and key[-1] != '.'):
                dic[key]=value
        return dic

    def count_types_preceding_word(self, ngrams, input1):
        count = 0
        for key in ngrams.keys():
            if(key[-1] == input1):
                count+=1
        return count
    
    def recursion_lower_ngram(self, input1, n):
        numerator = self.count_types_preceding_word(self.ngrams[n],input1[-1])
        denominator = len(self.ngrams[n])
        lambda_ = 0

        firsterm = max(0,numerator-0.75)/denominator
        #print(numerator, denominator, firsterm)
        if(n==1):
            lambda_ = (0.75 * len(self.ngrams[1]))/sum(self.ngrams[1].values())
        else:
            context_dict = self.get_words_succeeding_input(self.ngrams[n],input1[:-1],n)  
            if len(context_dict):
                lambda_ = (0.75*len(context_dict))/sum(context_dict.values())

        if lambda_!=0 and n!=1:
            return firsterm + lambda_ * self.recursion_lower_ngram(input1[1:],n-1)
        else:
            return firsterm + lambda_
    
    def highestOrder_ngram_prob(self, input1):
        n = self.n
        context_dict = self.get_words_succeeding_input(self.ngrams[n],input1[:-1],n)
        denominator = sum(context_dict.values())
        numerator = 0
        firsterm = 0
        if input1 in self.ngrams[n].keys():
            numerator = self.ngrams[n][input1]

        if len(context_dict) != 0:
            firsterm = max(0,numerator-0.75)/denominator
            lambda_ = (0.75*len(context_dict))/sum(context_dict.values()) 
            return firsterm + lambda_ * self.recursion_lower_ngram(input1[1:], n-1)
    
        return firsterm
    
    def calculate_probability(self, input1):
        prob = 1
        entropy = 0
        n = self.n
        if len(input1) < n :
            prob = self.recursion_lower_ngram(input1, len(input1))
            if prob == 0:
                prob = (len(self.ngrams[1]) * 0.75)/( sum(self.ngrams[1].values()))
            entropy = (prob * math.log2(prob))
        else:
            for j in range(0,len(input1)-n+1): 
                temp = self.highestOrder_ngram_prob(input1[j:j+n])
                if temp == 0:
                    temp = (len(self.ngrams[1]) * 0.75)/( sum(self.ngrams[1].values()))
                prob *= temp
                entropy += (prob * math.log2(prob))
        return prob, entropy
   
    def evaluate(self, test_data, filepath):
        f = open(filepath,'w+', encoding="utf8")
        total_perplexity = 0
        for i,sentence in enumerate(test_data):
            if(len(sentence) <= 0):
                continue
            sentence = tuple(sentence)
            prob, entropy = self.calculate_probability(sentence)
            #print(prob)
            perplexity = 2 ** (-1 * entropy) #Calculate_perplexity(prob, len(sentence))
            f.write(" ".join(sentence) + "\t" + str(perplexity) + "\n")
            
            total_perplexity += perplexity
        avg_perplexity = total_perplexity/len(test_data)
        f.write("averagePerplexity :\t" + str(avg_perplexity))
        f.close()

class WrittenBell():
    def __init__(self, ngrams = 4):
        self.n = ngrams
    
    def train(self, tokens):
        self.ngrams = [0]
        for i in range(1,self.n+1):
            ngrams = get_ngrams(tokens,i)
            self.ngrams.append(ngrams)
    
    def get_words_succeeding_input(self, ngrams, input1, n):
        dic={}
        for key,value in ngrams.items():
            if(key[:n-1] == input1 and key[-1] != '.'):
                dic[key]=value
        return dic
    
    
    def maximum_likelihood(self, input1, ngrams, n):
        p = 0
        try:
            p = ngrams[input1]/sum(ngrams.values())
        except:
            return 0
        return p
 
    def calc_back_off_weight(self,input1, ngrams, n):
        context_count = 0
        seq_count = 0
        
        context_dict = self.get_words_succeeding_input(ngrams, input1[:-1], n)
        if context_dict:
            context_count = len(context_dict)
            seq_count = sum(context_dict.values())
            return (context_count)/(context_count+seq_count)
        
        return 0
    
    def writtenBell(self,input1,n):
        max_likelihood = self.maximum_likelihood(input1, self.ngrams[n], n)
        #print("max_likelihood", max_likelihood)
        if(n==1):
            N1_count = len(self.ngrams[1])
            Total_unigrams = sum(self.ngrams[1].values())
            #print("N1_count: ", N1_count, "Total unigrams: ", Total_unigrams)
            return ((Total_unigrams/(Total_unigrams+N1_count))*max_likelihood) + (N1_count/((N1_count+Total_unigrams)*N1_count))
        
        backoff_weight = self.calc_back_off_weight(input1, self.ngrams[n], n)
        #print("backoff_weight", backoff_weight)
        if backoff_weight != 0:
            return ((1-backoff_weight)*max_likelihood) + (backoff_weight * self.writtenBell(input1[1:],n-1))

        return (1-backoff_weight)*max_likelihood
    
    def calculate_probability(self, input1):
        prob = 1
        entropy = 0
        n = self.n
        if len(input1) < n :
            prob = self.writtenBell(input1, len(input1))
            if(prob):
                entropy += (prob * math.log2(prob))
        else:
            for j in range(0,len(input1)-n+1): 
                temp = self.writtenBell(input1[j:j+n],n)
                if(temp):
                    prob *= temp
                    entropy += (prob * math.log2(prob))
        return prob,entropy    
    
    def evaluate(self, test_data, filepath):
        f = open(filepath,'w+', encoding="utf8")
        total_perplexity = 0
        for i,sentence in enumerate(test_data):
            if(len(sentence) <= 0):
                continue
            sentence = tuple(sentence)
            prob, entropy = self.calculate_probability(sentence)
            #print(prob)
            perplexity = 2 ** (-1 * entropy) #Calculate_perplexity(prob, len(sentence))
            f.write(" ".join(sentence) + "\t" + str(perplexity) + "\n")
            
            total_perplexity += perplexity
        avg_perplexity = total_perplexity/len(test_data)
        f.write("averagePerplexity :\t" + str(avg_perplexity))
        f.close()

def get_ngrams(tokens, n, pad_left=False, pad_right=False, pad_symbol = '</s>'):
    dic={}
    for sent in tokens:
        for i in range(len(sent)-n):
            ngram = tuple(sent[i:i+n])
            if ngram not in dic:
                dic[ngram]=1
            else:
                dic[ngram]+=1
    return dic 
