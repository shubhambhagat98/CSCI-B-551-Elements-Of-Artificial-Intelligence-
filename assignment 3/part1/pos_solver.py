###################################
# CS B551 Spring 2021, Assignment #3
#
# Your names and user ids: Henish Shah (henishah)
#                          Shubham Bhagat (snbhagat)
#                          Ameya Dalvi (abdalvi)
#
# (Based on skeleton code by D. Crandall)
#

import math
import numpy as np


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def __init__(self):
        self.emission_dict=dict()
        self.transition_dict=dict()
        self.initial_dict=dict()
        self.posterior_dict=dict()
        self.posterior_mcmc_dict = dict()
        self.ps = dict()
        self.pw = dict()
        self.emission_mcmc_dict = dict()
        self.transition_mcmc_dict = dict()
        self.observed=[]
        self.hidden = []
        
# This particular posterior function is referenced from https://github.com/Jashjeet/F19-B551-Residential-Elements-of-AI/blob/master/jsmadan-a3-master/part1/pos_solver.py
    def posterior(self, model, sentence, label):
        if model == "Simple":
            post_prob=0
            for i in range(len(sentence)):
                try:
                    if sentence[i] in self.posterior_dict.keys():
                        post_prob+=math.log(self.posterior_dict[sentence[i]][label[i]])
                except:
                    post_prob+=math.log(1e-20)
            return post_prob

        elif model == "HMM":
            post_prob = 0.0
            for i in range( len( sentence ) ) :
                if sentence[ i ] in self.emission_dict[label[i]].keys() :
                    t = self.emission_dict[label[ i ]][sentence[i]]
                    post_prob += math.log( t )
                else :
                    post_prob += math.log(0.00000000001 )
            
            prev_pos = label[0]
            for i in range(1,len(sentence)) :
                t = self.transition_dict[prev_pos][label[i]]
                try:
                    post_prob += math.log(t)
                except:
                    post_prob += math.log(0.00000000001 )
                prev_pos = label[ i ]
            
            return post_prob

        elif model == "Complex":
            
            post_prob = 0.0
            for i in range( len( sentence ) ) :
                if sentence[i] in self.emission_dict[label[i]].keys() :
                    t = self.ps[label[i]] * self.emission_dict[label[i]][sentence[i]]
                    post_prob += math.log( t )
                else :
                    post_prob += math.log(0.00000000001)
                    
            prev_pos = label[0]
            for i in range( 1 , len(label) ) :
                t = self.transition_dict[prev_pos][label[ i ]]
                try:
                    post_prob += math.log( t )
                except:
                    post_prob += math.log(0.000000001)
                prev_pos = label[ i ]        
            return post_prob
        else:
            print("Unknown algo!")

    # Do the training!
    #
    def train(self, data):
        # print(data[0])

        def ps(data):
            ps_dict=dict()
            count=0
            for i in data:
                count+=len(i[1])
                for j in range(len(i[1])):
                    if i[1][j] in ps_dict.keys():
                        ps_dict[i[1][j]]+=1
                    else:
                        ps_dict[i[1][j]]=1
            
            for i in ps_dict.keys():
                ps_dict[i]/=count

            return ps_dict
        
        def pw(data):
            pw_dict=dict()
            count=0
            for i in data:
                count+=len(i[0])
                for j in range(len(i[0])):
                    if i[0][j] in pw_dict.keys():
                        pw_dict[i[0][j]]+=1
                    else:
                        pw_dict[i[0][j]]=1
            
            for i in pw_dict.keys():
                pw_dict[i]/=count

            return pw_dict

        def posterior_prob(data):
            sw_dict=dict()
            for i in data:
                for j in range(len(i[0])):
                    if i[0][j] in sw_dict.keys():
                        sw_dict[i[0][j]]['count']+=1
                        if i[1][j] in sw_dict[i[0][j]].keys():
                            sw_dict[i[0][j]][i[1][j]]+=1
                        else:
                            sw_dict[i[0][j]][i[1][j]]=1
                    else:
                        sw_dict[i[0][j]]={i[1][j]:1,'count':1}

            for i in sw_dict.keys():
                for j in sw_dict[i].keys():
                    if j!='count':
                        sw_dict[i][j]=sw_dict[i][j]/sw_dict[i]['count']
                sw_dict[i].pop('count')
            return sw_dict

        def posterior_mcmc_prob(data):
            
            sw_mcmc_dict=dict()
            for i in data:
                for j in range(len(i[0])-1):
                    if i[0][j+1] in sw_mcmc_dict.keys():
                        sw_mcmc_dict[i[0][j+1]]['count']+=1
                        if i[1][j] in sw_mcmc_dict[i[0][j+1]].keys():
                            sw_mcmc_dict[i[0][j+1]][i[1][j]]+=1
                        else:
                            sw_mcmc_dict[i[0][j+1]][i[1][j]]=1
                    else:
                        sw_mcmc_dict[i[0][j+1]]={i[1][j]:1,'count':1}

            for i in sw_mcmc_dict.keys():
                for j in sw_mcmc_dict[i].keys():
                    if j!='count':
                        sw_mcmc_dict[i][j]=sw_mcmc_dict[i][j]/sw_mcmc_dict[i]['count']
                sw_mcmc_dict[i].pop('count')
            return sw_mcmc_dict


        def transition(data):
            pos=['noun','adj','adv','verb','det','adp','prt','conj','num','pron','x','.']
            transition_dict=dict()

            for i in data:
                for j in range(len(i[1])-1):
                    if i[1][j] in transition_dict.keys():
                        transition_dict[i[1][j]]['count']+=1
                        if i[1][j+1] in transition_dict[i[1][j]].keys():
                            transition_dict[i[1][j]][i[1][j+1]]+=1
                        else:
                            transition_dict[i[1][j]][i[1][j+1]]=1
                    else:
                        transition_dict[i[1][j]]={i[1][j+1]:1,'count':1}
            
            for i in transition_dict.keys():
                for j in transition_dict[i].keys():
                    if j!='count':
                        transition_dict[i][j]=transition_dict[i][j]/transition_dict[i]['count']
                transition_dict[i].pop('count')
            
            for i in transition_dict.keys():
                for j in pos:
                    if j not in transition_dict[i].keys():
                        transition_dict[i][j]=0
            
            return transition_dict


        def transition_mcmc(data):
            pos=['noun','adj','adv','verb','det','adp','prt','conj','num','pron','x','.']
            transition_mcmc_dict=dict()

            for i in data:
                for j in range(len(i[1])-2):
                    if i[1][j] in transition_mcmc_dict.keys():
                        transition_mcmc_dict[i[1][j]]['count']+=1
                        if i[1][j+2] in transition_mcmc_dict[i[1][j]].keys():
                            transition_mcmc_dict[i[1][j]][i[1][j+2]]+=1
                        else:
                            transition_mcmc_dict[i[1][j]][i[1][j+2]]=1
                    else:
                        transition_mcmc_dict[i[1][j]]={i[1][j+2]:1,'count':1}
            
            for i in transition_mcmc_dict.keys():
                for j in transition_mcmc_dict[i].keys():
                    if j!='count':
                        transition_mcmc_dict[i][j]=transition_mcmc_dict[i][j]/transition_mcmc_dict[i]['count']
                transition_mcmc_dict[i].pop('count')
            
            for i in transition_mcmc_dict.keys():
                for j in pos:
                    if j not in transition_mcmc_dict[i].keys():
                        transition_mcmc_dict[i][j]=0
            
            return transition_mcmc_dict


        def initial(data):
            initial_dict=dict()
            count=0
            for i in data:
                count+=1
                if i[1][0] in initial_dict.keys():
                    initial_dict[i[1][0]]+=1
                else:
                    initial_dict[i[1][0]]=1
            for i in initial_dict.keys():
                initial_dict[i]/=count
            return initial_dict


        def emission(data):
            emission_dict=dict()
            for i in data:
                for j in range(len(i[0])):
                    if i[1][j] in emission_dict.keys():
                        emission_dict[i[1][j]]['count']+=1
                        if i[0][j] in emission_dict[i[1][j]].keys():
                            emission_dict[i[1][j]][i[0][j]]+=1
                        else:
                            emission_dict[i[1][j]][i[0][j]]=1
                    else:
                        emission_dict[i[1][j]]={i[0][j]:1,'count':1}

            for i in emission_dict.keys():
                for j in emission_dict[i].keys():
                    if j!='count':
                        emission_dict[i][j]=emission_dict[i][j]/emission_dict[i]['count']
                emission_dict[i].pop('count')
            return emission_dict


        def emission_mcmc(data):
            emission_mcmc_dict=dict()
            for i in data:
                for j in range(len(i[0])-1):
                    if i[1][j] in emission_mcmc_dict.keys():
                        emission_mcmc_dict[i[1][j]]['count']+=1
                        if i[0][j+1] in emission_mcmc_dict[i[1][j]].keys():
                            emission_mcmc_dict[i[1][j]][i[0][j+1]]+=1
                        else:
                            emission_mcmc_dict[i[1][j]][i[0][j+1]]=1
                    else:
                        emission_mcmc_dict[i[1][j]]={i[0][j+1]:1,'count':1}

            for i in emission_mcmc_dict.keys():
                for j in emission_mcmc_dict[i].keys():
                    if j!='count':
                        emission_mcmc_dict[i][j]=emission_mcmc_dict[i][j]/emission_mcmc_dict[i]['count']
                emission_mcmc_dict[i].pop('count')
            return emission_mcmc_dict
            
        
        self.emission_dict=emission(data)
        self.transition_dict=transition(data)
        self.initial_dict=initial(data)
        self.posterior_dict=posterior_prob(data)
        self.ps = ps(data)
        self.pw = pw(data)
        self.emission_mcmc_dict = emission_mcmc(data)
        self.transition_mcmc_dict = transition_mcmc(data)
        self.posterior_mcmc_dict = posterior_mcmc_prob(data)
    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #
    def simplified(self, sentence):
        ans = []
        # find_dict={ value:key for key,value in self.ps}
        temp = [key for key in self.ps if self.ps[key]==max(self.ps.values())]
        top_s = temp[0]

        for i in list(sentence):
            if i in self.posterior_dict.keys():
                score = []
                temp_pos = []
                for j in self.posterior_dict[i].keys():
                    temp_pos.append(j)
                    score.append(self.posterior_dict[i][j])
                ans.append(temp_pos[score.index(max(score))])
            else:
                ans.append(top_s)
        return ans


    def hmm_viterbi(self, sentence):
        
        pos=['noun','adj','adv','verb','det','adp','prt','conj','num','pron','x','.'] 
        n = len(sentence)

        v_table = {'noun':[0]*n,'adj':[0]*n,'adv':[0]*n,'verb':[0]*n,'det':[0]*n,'adp':[0]*n,\
                    'prt':[0]*n,'conj':[0]*n,'num':[0]*n,'pron':[0]*n,'x':[0]*n,'.':[0]*n}

        which_table = {'noun':[0]*n,'adj':[0]*n,'adv':[0]*n,'verb':[0]*n,'det':[0]*n,'adp':[0]*n,\
                    'prt':[0]*n,'conj':[0]*n,'num':[0]*n,'pron':[0]*n,'x':[0]*n,'.':[0]*n}
        
        for p in pos:
            try:
                v_table[p][0] = -math.log(self.initial_dict[p]*self.emission_dict[p][sentence[0]])
                which_table[p][0]=p
            except KeyError:
                v_table[p][0] = -math.log(0.0000001)
                which_table[p][0]=p
        
        for i in range(1,n):
            for p in pos:
                temp=[]
                for p1 in pos:
                    try:
                        temp.append(v_table[p1][i-1]-math.log(self.transition_dict[p1][p]))
                    except:
                        temp.append(v_table[p1][i-1]-math.log(0.0000001))
                min_value=min(temp)
                which_table[p][i]=pos[temp.index(min_value)]
                try:
                    v_table[p][i]=min_value-math.log(self.emission_dict[p][sentence[i]])
                except:
                    v_table[p][i]=min_value-math.log(0.0000001)

        # Backtracking
        min_val=1000000000
        viterbi_seq = ['']*n
        for j in pos:
            if v_table[j][n-1]<min_val:
                min_val = v_table[j][n-1]
                viterbi_seq[n-1]=j
        for i in range(n-2,-1,-1):
            viterbi_seq[i]=which_table[viterbi_seq[i+1]][i+1]
      
        return viterbi_seq

    
    
    def complex_mcmc(self, sentence):

        pos=['noun','adj','adv','verb','det','adp','prt','conj','num','pron','x','.']

        def mcmc_inner_prob(sentence,sample):

            for i in range(len(sentence)):
                temp=[]
                for p in pos:
                    
                    if i==0:
                        try:
                            temp.append(self.emission_dict[p][sentence[i]]*self.emission_mcmc_dict[p][sentence[i+1]]\
                                *(self.transition_dict[p][sample[i+1]]*self.ps[p]/self.ps[sample[i+1]]))
                        except:
                            temp.append(0.000000000000001)
                    elif i==1:
                        try:
                            temp.append(self.emission_dict[p][sentence[i]]*self.emission_mcmc_dict[p][sentence[i+1]]\
                                *(self.transition_dict[p][sample[i+1]]*self.ps[p]/self.ps[sample[i+1]])\
                                        *(self.transition_dict[sample[i-1]][p]))
                        except:
                            temp.append(0.000000000000001)
                    elif 1<i<len(sentence)-2:
                        try:
                            temp.append(self.emission_dict[p][sentence[i]]*self.emission_mcmc_dict[p][sentence[i+1]]\
                                *(self.transition_dict[p][sample[i+1]]*self.ps[p]/self.ps[sample[i+1]])\
                                        *(self.transition_dict[sample[i-1]][p])\
                                            *(self.transition_mcmc_dict[sample[i-2]][p]))
                        except:
                            temp.append(0.000000000000001)
                    elif i==len(sentence)-2:
                        try:
                            temp.append(self.emission_dict[p][sentence[i]]*self.emission_mcmc_dict[p][sentence[i+1]]\
                                *(self.transition_dict[p][sample[i+1]]*self.ps[p]/self.ps[sample[i+1]])\
                                        *(self.transition_dict[sample[i-1]][p])\
                                            *(self.transition_mcmc_dict[sample[i-2]][p]))
                        except:
                            temp.append(0.000000000000001)
                    elif i==len(sentence)-1:
                        try:
                            temp.append(self.emission_dict[p][sentence[i]]*(self.transition_dict[sample[i-1]][p])\
                                            *(self.transition_mcmc_dict[sample[i-2]][p]))
                        except:
                            temp.append(0.00000000000001)
                temp=np.array(temp)
                temp/=temp.sum()
                sample[i]=np.random.choice(pos,p=temp)
            
            return sample

        count=500
        sample = [ "noun" ] * len(sentence)
        while count>0:
            count-=1
            sample = mcmc_inner_prob(sentence,sample)
        

        return sample



    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")

