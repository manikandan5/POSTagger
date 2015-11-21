###################################
# CS B551 Fall 2015, Assignment #5
#
# Your names and user ids:
#
# (Based on skeleton code by D. Crandall)
#
#
####
# Put your report here!!
####

import random
import math
from _collections import defaultdict

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    
    def __init__(self):
        self.dict_count_first_word={}
        self.dict_count_each_word={}
        self.dict_count_each_part_of_speech={}
        self.dict_count_part_of_speech_CP={}
        self.dict_count_word_part_of_speech={}

    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling
    def posterior(self, sentence, label):
        return 0

    # Do the training!
    #
    def train(self, data):
        self.dict_count_first_word,self.dict_count_each_word,self.dict_count_each_part_of_speech,self.dict_count_part_of_speech_CP,self.dict_count_word_part_of_speech=self.learning_dictionary(data)
        #print dict_count_first_word
        #print dict_count_each_word
        #print dict_count_each_part_of_speech
        #print dict_count_part_of_speech_CP
        #print dict_count_word_part_of_speech
        pass

    # Functions for each algorithm.
    #
    def naive(self, sentence):
        #dict_count_word_part_of_speech
        #print sentence
        tempkey=""
        word_used_as_part_of_speech="dd"
        CP_count=0
        output=[]
        part_of_speech=['ADJ','ADV','ADP','CONJ','DET','NOUN','NUM','PRON','PRT','VERB','X','.']
        #print self.dict_count_word_part_of_speech
        for i in range(0, len(sentence)):
            if(self.dict_count_each_word.has_key(sentence[i])):
                for j in range(0, len(part_of_speech)):
                    tempkey=sentence[i]
                    tempkey+="-"
                    tempkey+=part_of_speech[j].lower()
                    if(self.dict_count_word_part_of_speech[tempkey]> CP_count):
                        word_used_as_part_of_speech=part_of_speech[j].lower()
                        CP_count=self.dict_count_word_part_of_speech[tempkey]
                       
            else:
                word_used_as_part_of_speech="noun"
                
            #output=sentence[i]
            #output+="."
            output.append(word_used_as_part_of_speech)
            
        return [ [ output], [] ]
        #print output
        #Ground truth': [[('adv', '.', 'noun', 'verb', 'num', 'noun', 'prt', '.', 'verb', 'noun', 'noun', 'adp', 'det', 'noun', 'adp', 'det', 'noun', '.')], []]}
                
        #return [ [ [ "noun" ] * len(sentence)], [] ]

    def mcmc(self, sentence, sample_count):
        return [ [ [ "noun" ] * len(sentence) ] * sample_count, [] ]

    def best(self, sentence):
        return [ [ [ "noun" ] * len(sentence)], [] ]

    def max_marginal(self, sentence):
        return [ [ [ "noun" ] * len(sentence)], [[0] * len(sentence),] ]

    def viterbi(self, sentence):
        return [ [ [ "noun" ] * len(sentence)], [] ]
    
    def learning_dictionary(self,data):
        dict_count_first_word=defaultdict(int)
        dict_count_each_word=defaultdict(int)
        dict_count_each_part_of_speech=defaultdict(int)
        dict_count_part_of_speech_CP=defaultdict(int)
        dict_count_word_part_of_speech=defaultdict(int)
        for i in range(0,len(data)):
            dict_count_first_word[data[i][0][0]]=dict_count_first_word[data[i][0][0]]+1
            for j in range(0,len(data[i][0])):
                dict_count_each_word[data[i][0][j]]=dict_count_each_word[data[i][0][j]]+1  
                dict_count_each_part_of_speech[data[i][1][j]]=dict_count_each_part_of_speech[data[i][1][j]]+1
                if j<len(data[i][0])-1:
                    CP_part_of_speech=data[i][1][j]
                    CP_part_of_speech+="-"
                    CP_part_of_speech+=data[i][1][j+1]
                    dict_count_part_of_speech_CP[CP_part_of_speech]=dict_count_part_of_speech_CP[CP_part_of_speech]+1 
                    
                    
                    Word_part_of_speech=data[i][0][j]
                    Word_part_of_speech+="-"
                    Word_part_of_speech+=data[i][1][j]
                    dict_count_word_part_of_speech[Word_part_of_speech] = dict_count_word_part_of_speech[Word_part_of_speech]+1    
        return dict_count_first_word,dict_count_each_word,dict_count_each_part_of_speech,dict_count_part_of_speech_CP,dict_count_word_part_of_speech
        
    


    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It's supposed to return a list with two elements:
    #
    #  - The first element is a list of part-of-speech labelings of the sentence.
    #    Each of these is a list, one part of speech per word of the sentence.
    #    Most algorithms only return a single labeling per sentence, except for the
    #    mcmc sampler which is supposed to return 5.
    #
    #  - The second element is a list of probabilities, one per word. This is
    #    only needed for max_marginal() and is the marginal probabilities for each word.
    #
    def solve(self, algo, sentence):
        if algo == "Naive":
            return self.naive(sentence)
        elif algo == "Sampler":
            return self.mcmc(sentence, 5)
        elif algo == "Max marginal":
            return self.max_marginal(sentence)
        elif algo == "MAP":
            return self.viterbi(sentence)
        elif algo == "Best":
            return self.best(sentence)
        else:
            print "Unknown algo!"

