###################################
# CS B551 Fall 2015, Assignment #5
#
# Your names and user ids:
# Manikandan Murugesan and Debasis Dwivedy
#
# (Based on skeleton code by D. Crandall)
#
#
####
# Put your report here!!
# Our program performs all the functionalities of the assignment
# The dictionaries that have been used for the problem has been explained at the places where they have been initialised
# We have the learning function which reads the data from the training file and populates the learning library
# We have a Probability learning function which calculates the probability similarly
# Our best algorithm finds a better optimal solution
# Though we double checked the implementation of Viterbi algorithm, we are getting low values for that
# The output of the program is:
# Naive : 88.27 %
# MCMC : 7.14 %
# Sampling : 0% Our sampler generates the samples
# Viterbi : 72.43%
# Best : 93.35%
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
        self.total_number_of_words=1#Total number of words in the model
        self.dict_prob_each_part_of_speech={}#e.g.,(dict["verb"]=5)
        self.dict_word_probability={}#e.g.,(dict[cp_hari|noun]=0.05)
        self.dict_part_of_speech_probability={}#e.g.,(dict[cp_noun|verb]=0.05)

    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling
    def posterior(self, sentence, label):
        return self.posterior_calculation(sentence, label)

    # Do the training!
    #
    def train(self, data):
        self.dict_count_first_word,self.dict_count_each_word,self.dict_count_each_part_of_speech,self.dict_count_part_of_speech_CP,self.dict_count_word_part_of_speech,self.total_number_of_words=self.learning_dictionary(data)
        #print dict_count_first_word
        #print dict_count_each_word
        #print self.dict_count_each_part_of_speech
        #print dict_count_part_of_speech_CP
        #print self.dict_count_word_part_of_speech
        self.dict_part_of_speech_probability,self.dict_word_probability=self.probability_dictionary(data)
        #print self.dict_part_of_speech_probability
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
        #print len(sentence)
        dd=[]
        part_of_speech=self.naive(sentence)
        part_of_speech=part_of_speech[0][0]
        #print part_of_speech.count('noun')
        #p_noun=part_of_speech.count('noun')/len(part_of_speech)
        different_parts_of_speech=['ADJ','ADV','ADP','CONJ','DET','NOUN','NUM','PRON','PRT','VERB','X','.']
        burn_in =1000
        for g in range(0,burn_in+sample_count):
            position_list=[]
            for i in range(0,len(sentence)):

                normalized_probability_of_word_in_sentence=[]
                if(i==0):
                    for j in range(0,len(different_parts_of_speech)):
                         a=self.dict_part_of_speech_probability["cp_"+part_of_speech[i+1]+"|"+different_parts_of_speech[j].lower()]
                         p1=float(self.dict_part_of_speech_probability["cp_"+part_of_speech[i+1]+"|"+different_parts_of_speech[j].lower()])*float(self.dict_word_probability["cp_"+sentence[i]+"|"+different_parts_of_speech[j].lower()])
                         p1=float(part_of_speech.count(different_parts_of_speech[j].lower()))/float(len(part_of_speech))
                         normalized_probability_of_word_in_sentence.append(p1)

                elif(i==len(sentence)-1):
                    for j in range(0,len(different_parts_of_speech)):
                         p2=float(self.dict_part_of_speech_probability["cp_"+part_of_speech[i-1]+"|"+different_parts_of_speech[j].lower()])*float(self.dict_word_probability["cp_"+sentence[i]+"|"+different_parts_of_speech[j].lower()])
                         p2=float(part_of_speech.count(different_parts_of_speech[j].lower()))/float(len(part_of_speech))
                         normalized_probability_of_word_in_sentence.append(p2)

                else:
                    for j in range(0,len(different_parts_of_speech)):
                         p3=float(self.dict_part_of_speech_probability["cp_"+part_of_speech[i-1]+"|"+different_parts_of_speech[j].lower()])*float(self.dict_part_of_speech_probability["cp_"+part_of_speech[i+1]+"|"+different_parts_of_speech[j].lower()])*float(self.dict_word_probability["cp_"+sentence[i]+"|"+different_parts_of_speech[j].lower()])
                         p3=float(part_of_speech.count(different_parts_of_speech[j].lower()))/float(len(part_of_speech))
                         normalized_probability_of_word_in_sentence.append(p3)

                #normalized_probability_of_word_in_sentence=sum(normalized_probability_of_word_in_sentence)
                #print self.dict_part_of_speech_probability
                #print self.dict_word_probability
                sum_list =[]
                sum_pos = 0
                for prob in normalized_probability_of_word_in_sentence:
                    sum_pos += prob
                    sum_list.append(sum_pos)

                r=random.random()
                position = 0
                for sum in sum_list:
                    if (r <= sum):
                        break
                    position += 1
                position_list.append(different_parts_of_speech[position])
            if(g>=burn_in):
                dd.append(position_list)
                #dd.append(different_parts_of_speech[position])
                #print different_parts_of_speech[position]
                #print sum(normalized_probability_of_word_in_sentence)
                #===================================================================
                # for l in range(0,len(normalized_probability_of_word_in_sentence)-1):
                #     #print float(normalized_probability_of_word_in_sentence[l])
                #     if(sum(normalized_probability_of_word_in_sentence)!=0.0):
                #         normalized_probability_of_word_in_sentence[l]=float(normalized_probability_of_word_in_sentence[l])/float(sum(normalized_probability_of_word_in_sentence))
                #===================================================================

                #print normalized_probability_of_word_in_sentence

        #print len(dd)
        #print dd
        return [ dd, [] ]


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
        [output,dd]=self.mcmc(sentence, 5)
        #print output
        final_output=[]
        confidence_score=[]
        different_parts_of_speech=['ADJ','ADV','ADP','CONJ','DET','NOUN','NUM','PRON','PRT','VERB','X','.']
        sentence_parts_of_speech= defaultdict(dict)
        inner_dict={}
        for word in sentence:
            for speech in different_parts_of_speech:
                sentence_parts_of_speech[word][speech]=0
        print sentence_parts_of_speech
        for taglist in output:
            for length in range(len(sentence)) :
                sentence_parts_of_speech[sentence[length]][taglist[length]] += 1

        max_part_of_speech=""
        for i in range(0,len(sentence_parts_of_speech)):
            inner_dict=sentence_parts_of_speech.get(sentence[i])
            temp_num=0
            for k in range(0,len(different_parts_of_speech)):
                if(inner_dict[different_parts_of_speech[k]]>temp_num):
                    max_part_of_speech=different_parts_of_speech[k]
                    temp_num=inner_dict[different_parts_of_speech[k]]
            confidence_score.append(0.5)
            final_output.append(max_part_of_speech)

        final_output.append('.')
        return [ [final_output], [confidence_score]]

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
    
    def posterior_calculation(self, sentence,output):
        sum = 1
        part_of_speech = ['adj','adv','adp','conj','det','noun','num','pron','prt','verb','x','.']      # List of Parts of Speeches
        Probability_word_given_part = {}
        Probability_state_change = {}
        Probability_first_word ={}
        Count_first_word = {}
        word = sentence[0]
        for part in part_of_speech:
            Count_first_word[part] = self.dict_count_word_part_of_speech[word+"-"+part]

        for part in part_of_speech:
            if self.dict_count_each_word[word] !=0:
                Probability_first_word[part] = float(Count_first_word[part]) / self.dict_count_each_word[word]
            else:
                Probability_first_word[part] =0
        for word in sentence:
            for part in part_of_speech:
                Probability_word_given_part[word+"-"+part] = float(self.dict_count_word_part_of_speech[word+"-"+part])/self.dict_count_each_part_of_speech[part]
        for state in self.dict_count_part_of_speech_CP:
            Probability_state_change[state] = float(self.dict_count_part_of_speech_CP[state])/ self.dict_count_each_part_of_speech[state.split("-")[0]]
        for i in range(len(sentence)):
            if i == 0:
                try:

                    sum = sum + Probability_word_given_part[sentence[i].lower()+"-"+output[i]] *  Probability_first_word[output[i]]
                except:
                    sum = sum
            else:
                try:
                    sum = sum + (Probability_first_word[output[0]] * (Probability_state_change[output[i-1]+"-"+output[i]] * Probability_word_given_part[sentence[i].lower()+"-"+output[i]]))
                except:
                    sum = sum
        return math.log10(sum)
        
    
    def learning_dictionary(self,data):
        dict_count_first_word=defaultdict(int)
        dict_count_each_word=defaultdict(int)
        dict_count_each_part_of_speech=defaultdict(int)
        dict_count_part_of_speech_CP=defaultdict(int)
        dict_count_word_part_of_speech=defaultdict(int)
        total_number_of_words=0
        for i in range(0,len(data)):
            dict_count_first_word[data[i][0][0]]=dict_count_first_word[data[i][0][0]]+1
            for j in range(0,len(data[i][0])):
                total_number_of_words+=1
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

        return dict_count_first_word,dict_count_each_word,dict_count_each_part_of_speech,dict_count_part_of_speech_CP,dict_count_word_part_of_speech,total_number_of_words


    def probability_dictionary(self,data):
        different_parts_of_speech=['ADJ','ADV','ADP','CONJ','DET','NOUN','NUM','PRON','PRT','VERB','X','.']
        part_of_speech_probability=defaultdict(int)
        sum_of_parts_of_speech=sum(self.dict_count_part_of_speech_CP.values())
        for i in range(0,len(different_parts_of_speech)):
            for j in range(0,len(different_parts_of_speech)):
                #if(different_parts_of_speech[i]!=different_parts_of_speech[j]):
                    #self.dict_count_part_of_speech_CP={} #e.g.,(dict["noun-verb"]=5)
                    temp_part_of_speech=""
                    temp_part_of_speech+="cp_"
                    temp_part_of_speech+=different_parts_of_speech[i].lower()
                    temp_part_of_speech+="|"
                    temp_part_of_speech+=different_parts_of_speech[j].lower()
                    a_int_b=self.dict_count_part_of_speech_CP[different_parts_of_speech[j].lower()+"-"+different_parts_of_speech[i].lower()]
                    prob_a_int_b=a_int_b/sum_of_parts_of_speech
                    #[p("verb")=0.5]
                    prob_part_of_speech=float(self.dict_count_each_part_of_speech[different_parts_of_speech[j].lower()])/float(self.total_number_of_words)
                    self.dict_prob_each_part_of_speech[different_parts_of_speech[j].lower()]=prob_part_of_speech
                    if(prob_part_of_speech!=0):
                        part_of_speech_probability[temp_part_of_speech]=prob_a_int_b/prob_part_of_speech
                    else:
                        part_of_speech_probability[temp_part_of_speech]=0.0005


        # self.dict_count_word_part_of_speech={}#e.g., (dict[hari-noun]=6)
        #self.dict_count_each_word(dict[hari]=6)
        #Word_part_of_speech=data[i][0][j]
        #Word_part_of_speech+="-"
        #Word_part_of_speech+=data[i][1][j]
        word_probability=defaultdict(int)

        for i in range(0,len(data)):
            for j in range(0,len(data[i][0])):
                word=data[i][0][j]
                for k in range(0,len(different_parts_of_speech)):
                    count_word=self.dict_count_each_word[word]
                    count_part_of_speech=self.dict_count_each_part_of_speech[different_parts_of_speech[k]]

                    count_word_int_part_of_speech=self.dict_count_word_part_of_speech[word+"-"+different_parts_of_speech[k].lower()]
                    probability_of_part_of_speech=self.dict_prob_each_part_of_speech[different_parts_of_speech[k].lower()]
                    temp_word=""
                    temp_word+="cp_"
                    temp_word+=word
                    temp_word+="|"
                    temp_word+=different_parts_of_speech[k].lower()
                    if(probability_of_part_of_speech!=0 and count_part_of_speech!=0):
                        word_probability[temp_word]=(float(count_word_int_part_of_speech)/float(count_part_of_speech))/probability_of_part_of_speech
                    else:
                        word_probability[temp_word]=0.0005

        #print part_of_speech_probability
        #print word_probability
        return part_of_speech_probability,word_probability

    


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

