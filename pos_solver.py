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
        self.dict_count_first_word={} #p(s1)
        self.dict_count_each_word={} #Number of times a word occurs in the model data
        self.dict_count_each_part_of_speech={} #e.g.,(dict["noun"]=3)
        self.dict_count_part_of_speech_CP={} #e.g.,(dict["noun-verb"]=5)
        self.dict_count_word_part_of_speech={}#e.g., (dict[hari-noun]=6)

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
        #print self.dict_count_each_part_of_speech
        #print dict_count_part_of_speech_CP
        #print self.dict_count_word_part_of_speech
        pass

    # Functions for each algorithm.
    #
    def naive(self, sentence):
        #dict_count_word_part_of_speech
        #print sentence
        tempkey=""
        word_used_as_part_of_speech="dd"
        output=[]
        part_of_speech=['ADJ','ADV','ADP','CONJ','DET','NOUN','NUM','PRON','PRT','VERB','X','.']
        #print self.dict_count_word_part_of_speech
        for i in range(0, len(sentence)):
            if(self.dict_count_each_word.has_key(sentence[i])):
                CP_count=0
                for j in range(0, len(part_of_speech)):
                    tempkey=sentence[i]
                    tempkey+="-"
                    tempkey+=part_of_speech[j].lower()
                    if(self.dict_count_word_part_of_speech[tempkey]> CP_count):
                        word_used_as_part_of_speech=part_of_speech[j].lower()
                        CP_count=self.dict_count_word_part_of_speech[tempkey]
                       
            else:
                CP_count=0
                for j in range(0, len(part_of_speech)):
                    if(self.dict_count_each_part_of_speech[part_of_speech[j].lower()]>CP_count):
                        CP_count=self.dict_count_each_part_of_speech[part_of_speech[j].lower()]
                        word_used_as_part_of_speech=part_of_speech[j].lower()
                
            #output=sentence[i]
            #output+="."
            output.append(word_used_as_part_of_speech)
            
        return [ [ output], [] ]
        #print output     
        #return [ [ [ "noun" ] * len(sentence)], [] ]

    def mcmc(self, sentence, sample_count):
        return [ [ [ "noun" ] * len(sentence) ] * sample_count, [] ]

    def best(self, sentence):
        word_used_as_part_of_speech="dd"
        output=[]
        punctuation = [',','.','\'','"','!']
        part_of_speech=['ADJ','ADV','ADP','CONJ','DET','NOUN','NUM','PRON','PRT','VERB','X','.']
        for i in range(0, len(sentence)):
            if sentence[i] in punctuation:
                word_used_as_part_of_speech = "."
            else:
                if(self.dict_count_each_word.has_key(sentence[i])):
                    CP_count=0
                    for j in range(0, len(part_of_speech)):
                        tempkey=sentence[i]
                        tempkey+="-"
                        tempkey+=part_of_speech[j].lower()
                        if(self.dict_count_word_part_of_speech[tempkey]> CP_count):
                            word_used_as_part_of_speech=part_of_speech[j].lower()
                            CP_count=self.dict_count_word_part_of_speech[tempkey]
                       
                else:
                    CP_count=0
                    for j in range(0, len(part_of_speech)):
                        if(self.dict_count_each_part_of_speech[part_of_speech[j].lower()]>CP_count):
                            CP_count=self.dict_count_each_part_of_speech[part_of_speech[j].lower()]
                            word_used_as_part_of_speech=part_of_speech[j].lower()

            output.append(word_used_as_part_of_speech)
            
        return [ [ output], [] ]
	#return [ [ [ "noun" ] * len(sentence)], [] ]

    def max_marginal(self, sentence):
        return [ [ [ "noun" ] * len(sentence)], [[0] * len(sentence),] ]

    def viterbi(self, sentence):
        part_of_speech = ['adj','adv','adp','conj','det','noun','num','pron','prt','verb','x','.']      # List of Parts of Speeches
        Count_first_word = {}                                                                           # Dictionary that contains respective count of the first word in different parts of speech
        Probability_first_word = {}                                                                     # Probability of first part being the part of speech in the key
        Probability_state_change = {}                                                                   # Probability of status changing from state 1 to state 2
        Probability_word_given_part = {}                                                                # Probability that the word given a particular part of speech
        punctuation = [',','.','\'','"','!','`']                                                        # Punctuation list
        word = sentence[0]                                                                              # Temporary initialisation variables

        #Loop to find the count of the first word being respective part of speech in the key and to find the total occurence of the word
        for part in part_of_speech:
            Count_first_word[part] = self.dict_count_word_part_of_speech[word+"-"+part]

        #Loop to find the probability for the first word
        for part in part_of_speech:
            if self.dict_count_each_word[word]!=0:
                Probability_first_word[part] = float(Count_first_word[part]) / self.dict_count_each_word[word]
            else:
                Probability_first_word[part]=0

        #Probability for the state to change from one to another
        for state in self.dict_count_part_of_speech_CP:
            Probability_state_change[state] = float(self.dict_count_part_of_speech_CP[state])/ self.dict_count_each_part_of_speech[state.split("-")[0]]

        #Probability to find the word given that it is a particular part of speech
        for word in sentence:
            for part in part_of_speech:
                Probability_word_given_part[word+"-"+part] = float(self.dict_count_word_part_of_speech[word+"-"+part])/self.dict_count_each_part_of_speech[part]

        prob = 0
        temp = " "
        wordlist = []
        for word in sentence:
            if word in punctuation:
                wordlist.append('.')
            else:
                #Loop to find the maximum Viterbi for the first word
                if (wordlist == []):
                    for part in part_of_speech:
                        if (Probability_first_word[part] *  Probability_word_given_part[sentence[0]+"-"+part]>prob):
                            prob = Probability_first_word[part] *  Probability_word_given_part[sentence[0]+"-"+part]
                            temp = part
                    wordlist.append(temp)
                else:       #Loop for the second word onwards
                    probability = 0
                    for part in part_of_speech:
                        try:
                            if (prob * Probability_word_given_part[word+"-"+part] * Probability_state_change[temp+"-"+part]>probability):
                                probability = prob * Probability_word_given_part[word+"-"+part] * Probability_state_change[temp+"-"+part]
                                prob = probability
                                temp = part
                        except:
                            temp="noun"
                    wordlist.append(temp)
        return [ [ wordlist], [] ]
    
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

