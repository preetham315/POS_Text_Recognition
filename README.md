# Part-1 - Parts of Speech Tagging

## Simplified Bayes Net

### Formula

* P(S/W)= (P(W/S)*P(S))/P(W)

### Approach

For this approach we are expected to find the probability of a part of speech given word. So using bayes theorem we calculate the posterior i.e P(W/S) and prior P(S). P(W) can be neglected as it will be very small when compared to the list of total words. So for
calculating the posterior we have constructed a frequencies dictionary which has a word and the in the keys we will be having the dict of all the possible parts of speech. So we are going to divide this by totol frequency of that particular pos .Then this output is multiplied to the P(S) which is the ratio of occurence of a particular pos to tolat length of words in the given data. 

So here we've encountered problems where in the word is not present in the test data so to handle this we have given some basic rules of grammer for the most occuring parts of speech and by default we are considering the rest to be be may be noun with a probability of 0.2.

Some of the important dicts and variables to be noted are:
* frequencies: gives us the freq of word beign that particular pos 
* parts of speech : gives us the freq of ocurance of a parts of speech
* words: gives us the total number of words given in the training data set

* Obtained accuaracy is 49.28%

## Viterbi- HMM

### Formula 
* P(S/W)= max(Transition_probability)* P(Si/W)--> Emission probabity

### Appraoch

For this approach we have started initialyy by creating a viterbi table which is a dict. Then here the states are pasrts of speech and the observed values are words. So firstly, we initialised the viterbi table with all the initial values for pos. Then moving on we calculated the transition probabilities of respective states and used the max of all these values to mulitply with the emission probability. Finally storing the probability and the previous state. After doing this we iterated over the v_table to get the best possible sequence to generated for the observed sequence.

We only considered the previous state as in HMM the crux is that we only consider just the prior state for the current state. Used most of the code that i did for in class assignment

Some important variables and dicts to be noted are:

* V_talbe: stores the probability and the previous state
* Max_prob : gives the final max probaility
* opt: final ouput sequence obtained that has highest probability


* Obtained accuaracy is 70.30%

## Markov Chain Monte Carlo : Gibbs Sampling

### Approach

 In this approach firstly we tried calculating hte transition probabilities from states n to n+2 as every state that is current is dependent on the previous two states and the emission from the observed to hidden states is also dependent on the current state and the previous state. WE tried creating a dictionary that has the transition proababilities for the n, n+2 pos but after that we struggled to do the sampling and obtain the stationary distribution from where we can ignore the previous burn in values and consider the balanced probabilities for which we have high efficiency. Attempts were made to solve for the balanced proabability but the time to run ofr the least amout of smaples is also exceeding the 10 min interval mentioned and these were the final tries made to calcualte the MCMC.

## Reading Text

### Problem Statement: 
There are many techniques for image processing which can be used to get the required characters from the image that is given. But here we try to find the characters in the image using Simple Bayes Natwork and HMMs. Here the images are noisy and our main challenge is figureout the letters from the image with as much as noise can be removed

### Approach: 

In our first approach, we have used Simple Bayes Network to find the words formt he noisy image. At first we train our algorithm such that it can easily find the given text from given images. Our training set consists of Lower case characters(26), Upper case characters(26), numbers(10) and special symbols (,.-!?\"' ). Once our image is converted, it will be consisiting of '*' and ' '. The whole letter/symbol is in these two symbols based on which we derive the character. Initially we create a dictionary for the test data with indicies of all the characters in it. Then for each character we make a count of * and ' ' respectively. Once the dictionary is created, our next task was to extract symbols and numbers individually form the constructed dictionary.

For the ease of our code, we categorize the characters into we have 3 dictionaries(original, symbols and numbers). If we are able to find a character as a number or a symbol it will be added to the respective dictionary and removed from the original dictionary. There are still some character which are misread, so to get the right values we calculate the symbols and numbers based on threshold values

### Result:
Given: SUPREME COURT OF THF UNITED STATES
Simple: SUPREME COURT OF THF UN.TED STATES
HMM: Sample simple result


## References (referred the following pages to better understand the code for viterbi algorithm and rest of the parts)

* https://stackoverflow.com/questions/32103458/python-viterbi-algorithm
* http://www.adeveloperdiary.com/data-science/machine-learning/implement-viterbi-
algorithm-in-hidden-markov-model-using-python-and-r/
* https://www.pythonpool.com/viterbi-algorithm-python/ (code-reference)
* https://stackoverflow.com/questions/9729968/python-implementation-of-viterbi-
algorithm

* https://medium.com/analytics-vidhya/part-of-speech-tagging-what-when-why-and-how-9d250e634df6
* https://medium.com/analytics-vidhya/pos-tagging-using-conditional-random-fields-92077e5eaa31
* https://medium.com/codex/a-probabilistic-approach-to-pos-tagging-hmm-a557f963e159
* https://etn-sas.eu/2020/09/23/part-of-speech-tagging-using-hidden-markov-models/
* https://www.tweag.io/blog/2019-10-25-mcmc-intro1/
* https://www.tweag.io/blog/2020-01-09-mcmc-intro2/








