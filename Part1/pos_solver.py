
import random
import math

class Solver:
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def posterior(self, model, sentence, label):
        if model == "Simple":
            post = 1.0
            for s,l in zip(sentence,label):
                temp = l+"|"+s
                if temp in self.posterior_SW.keys():
                    post = float(post) * self.posterior_SW[l+"|"+s]
            return post
        elif model == "HMM":
            prob_hmm = float(self.parts_of_speech[label[0]]/sum(self.parts_of_speech.values()))
            t = 1.0
            e= 1.0
            for i in range(len(label)):
                e = float(e)*(self.get_init_emission(sentence[i],label[i]))
                if i!=0:
                    t=float(t)*self.transition_prob[label[i-1]][label[i]]
            return float(prob_hmm*t*e)
        elif model == "Complex":
            return -999
        else:
            print("Unknown algo!")

    # Do the training!
   
    def train(self, data):
        words=0
        parts_of_speech= {}
        for i in range(len(data)):
            words +=  len(data[i][0])
        self.words= words
        # word_freq = {}
        # for i in range(len(data)):
        #     for j in range(len(data[i][0])):
        #         if data[i][0][j] in word_freq:
        #             word_freq[j] +=1
        #         else:
        #             word_freq[j]=1
        # self.word_freq= word_freq
        for i in range(len(data)):
            for j in range(len(data[i][1])):
                # print(data[i][1][j])
                if data[i][1][j] in parts_of_speech:
                    parts_of_speech[data[i][1][j]]+=1
                else:
                    parts_of_speech[data[i][1][j]]=1
        self.parts_of_speech= parts_of_speech
        frequencies = {}
        for line in data:
            # print (line)
            text = line[0]
            pos = line[1]
            for i in range(0, len(text)):
                if text[i] in frequencies.keys():
                    if pos[i] in frequencies[text[i]].keys():
                        frequencies[text[i]][pos[i]] += 1
                    else:
                        frequencies[text[i]][pos[i]] = 1
                else:
                    frequencies[text[i]] = {}
                    frequencies[text[i]][pos[i]] = 1
        self.frequencies= frequencies
        #print(frequencies)

        #calculating transition probability
        transition_prob ={}
        #print(parts_of_speech)
        for i in self.parts_of_speech.keys():
                for j in self.parts_of_speech.keys():
                    if i in transition_prob.keys():
                            transition_prob[i][j] = 0
                    else:
                        transition_prob[i] = {}
                        transition_prob[i][j] = 0

        for line in data:
            pos = line[1]
            prev_pos = pos[0]
            for i in range(1,len(pos)):
                transition_prob[prev_pos][pos[i]] +=1
                prev_pos = pos[i] 
        # print(transition_prob)
        # print(self.frequencies)
        self.transition_prob = transition_prob 
    def find_pos(self,word):
        if (list(word)[-2:] == list("ed") or  list(word)[-3:] == list("ify") or list(word)[-3:] == list("ing") ) :
            return "verb"

        elif (list(word)[-4:] == list("less") or list(word)[-4:] == list("like") or  list(word)[-4:] == list("able")
            or list(word)[-3:] == list("ful") or
            list(word)[-2:] == list("ic") or list(word)[-3:] == list("ish") or list(word)[-3:] == list("ive")or list(word)[-3:] == list("ous")):
            return "adj"

        elif (list(word)[-2:] == list("ly") ):
            return "adv"

        elif (list(word)[-2:] == list("'s") or list(word)[-3:] == list("ist") or list(word)[-3:] == list("ion") or
            list(word)[-4:] == list("ment")):
            return "noun"
        else:
            return "noun_maybe"
    
    def get_init_emission(self,word,pos):
        if word in self.frequencies.keys():
            if pos in self.frequencies[word].keys():
                return self.frequencies[word][pos]/sum(self.frequencies[word].values())
            else:
                prob_val = self.find_pos(word)
                if prob_val == "noun_maybe":
                    return 0.2
                return 0.7
        else:
            prob_val = self.find_pos(word)
            if prob_val == "noun_maybe":
                return 0.2
            return 0.7


    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #
    def simplified(self, sentence):
        posterior_SW={}
        count = 0
        for word in sentence:
            max_value =-999999
            if word in self.frequencies.keys():
                for i in self.frequencies[word].keys():
                    new_val = (self.frequencies[word][i]/(self.words))
                    if new_val > max_value:
                        #print(word,i, self.frequencies[word][i])
                        max_value = new_val
                posterior_SW[str(count) +"|"+i+ "|" + word] = max_value
                #print(posterior_SW)
                count = count+1
            else:
                pos_new = self.find_pos(word)
                if pos_new == "noun_maybe":
                    posterior_SW[str(count) +"|"+"noun"+ "|" + word]  = 0.2
                    count = count+1
                else:
                    posterior_SW[str(count) +"|"+pos_new+ "|" + word] = 0.9
                    count = count+1
        result =[]
        for pos in posterior_SW.keys():
            pos_new = pos.split("|")[1]
            # print(pos.split("|")[2]+ "---" +pos.split("|")[1] + "---"+ pos.split("|")[0])
            result.append(pos_new)
        
        self.posterior_SW = posterior_SW
        return result
        # for word in sentence:
        #     pos_words = []

    def hmm_viterbi(self, sentence):
        V_table = [{}]
        for i in self.parts_of_speech.keys():
            V_table[0][i] = {"prob":(self.parts_of_speech[i]/sum(self.parts_of_speech.values())) * self.get_init_emission(sentence[0],i), "prev":None}
        # print(V_table)
        for t in range(1, len(sentence)):
            V_table.append({})
            for i in self.parts_of_speech.keys():
                first_pos = list(self.parts_of_speech.keys())[0]
                max_tr_prob = V_table[t-1][first_pos]["prob"] * (self.transition_prob[first_pos][i]/sum(self.transition_prob[i].values()))
                prev_state_selected =  first_pos
                for j in list(self.parts_of_speech.keys())[1:]:
                    temp_prob = V_table[t-1][j]["prob"] * (self.transition_prob[j][i]/sum(self.transition_prob[i].values()))
                    if temp_prob> max_tr_prob:
                        max_tr_prob = temp_prob
                        prev_state_selected = j
                # print("maxxx",max_tr_prob)
                # print("i",i)
                # print(sentence[t])
                max_prob = max_tr_prob * self.get_init_emission(sentence[t],i)
                V_table[t][i] = {"prob":max_prob,"prev":prev_state_selected}
            # print(V_table)
        opt =[]
        max_prob = -9999999999
        best_st = None
        for i,j in V_table[-1].items():
            # print(i)
            # print(j)
            if j["prob"]>max_prob:
                max_prob = j["prob"]
                best_st = i
        opt.append(best_st)
        previous = best_st
        for t in range(len(V_table)-2,-1,-1):
            opt.insert(0, V_table[t + 1][previous]["prev"])
            previous = V_table[t + 1][previous]["prev"]
        return opt
    def complex_mcmc(self, sentence):
        return [ "noun" ] * len(sentence)



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

