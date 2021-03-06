#%% Imports
import numpy as np
import pandas as pd
import nltk
nltk.download('punkt')

#%% Likelihood Table

# create lists for words and parts of speech
words = []
pos = []

# read training file and add all words and parts of speech to respective lists
with open('data/training.pos', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line != '':
            words.append(line.split("\t")[0].lower().strip())
            pos.append(line.split("\t")[1].lower().strip())
        else:
            pos.append('start')

# create a list of unique words and parrs of speech
uniqueWords = sorted(set(words))
uniquePos = sorted(set(pos))

# put the 'start' part of speech at end 
uniquePos.remove('start')
uniquePos.append('start')

# create word to part of speech likelihood table
likelihood = pd.DataFrame(index = uniqueWords, columns = uniquePos)

# re-read training file but this time counting the amount of times a word in a part of speech occurs
with open('data/training.pos', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line != '':
            word = line.split('\t')[0].lower().strip()
            part = line.split('\t')[1].lower().strip()
            if pd.isnull(likelihood.loc[word, part]):
                likelihood.loc[word, part] = 1
            else:
                likelihood.loc[word, part] += 1

# go through each word normalizing its probability to add up to 1, mark nulls as 0
for i in range(len(likelihood)):
    count = np.nansum(likelihood.iloc[i])
    for j in range(len(likelihood.iloc[i])):
        if not pd.isnull(likelihood.iloc[i, j]):
            likelihood.iloc[i, j] /= count
        else:
            likelihood.iloc[i, j] = 0
            
# create and add an 'out of vocabulary' row and add onto table
oov = np.full(len(likelihood.iloc[0]), 1/len(likelihood.iloc[0]))
likelihood.loc['oov'] = oov

#%% Hidden Markov Model

# create bigrams of parts of speech using nltk
bigrams = list(nltk.bigrams(pos))

# create markov matrix with unique parts of speech
markov = pd.DataFrame(index = uniquePos, columns = uniquePos)

# count pos transitions, except for transitioning to 'start'
for current, transition in bigrams:
    if transition != 'start':
        if pd.isnull(markov.loc[current, transition]):
            markov.loc[current, transition] = 1
        else:
            markov.loc[current, transition] += 1

# normalize probabilities per row such that they add to 1
for i in range(len(markov)):
    count = np.nansum(markov.iloc[i])
    for j in range(len(markov.iloc[i])):
        if not pd.isnull(markov.iloc[i, j]):
            markov.iloc[i, j] /= count
        else:
            markov.iloc[i, j] = 0
        

#%% POS Tagging

# read in test set
with open('data/test.words', 'r') as f:
    lines = f.readlines()
    lines.insert(0, '\n')
    lines.append('\n')

# instantiate variables to be used in algorithm
first = True
viterbi = 0
wordsList = 0

# clear output file
open('oldOutput.txt', 'w').close()

# tagging algorithm
with open('oldOutput.txt', 'a') as f:
    # iterate through each word
    for word in lines:
        orig = word.strip()  # track original word with \n
        word = word.strip().lower()  # track lowercase word to use with likelihood table
        if word == '':
            if not first:
                maxTuple = (0,0)
                posList = []
                index = 0
                # find largest probability in the last column
                for row in range(len(viterbi)):
                    if viterbi.iloc[row,-1][0] > maxTuple[0]:
                        maxTuple = viterbi.iloc[row,-1]
                        index = row
                # insert parts of speech into list
                posList.insert(0,uniquePos[index])
                posList.insert(0,uniquePos[maxTuple[1]])
                # iterate through viterbi dataframe backwards looking at indices to traverse parts of speech
                for backwards in range(len(viterbi.iloc[0])-2,0,-1):
                    maxTuple = viterbi.iloc[maxTuple[1],backwards]
                    posList.insert(0,uniquePos[maxTuple[1]])
                # remove start part of speech from list
                del wordsList[0]
                del posList[0]
                # write words and respective parts of speech into file
                for i in range(len(posList)):
                    f.write(wordsList[i] + '\t' + posList[i].upper() + '\n')
                f.write('\n')
            first = False
            viterbi = pd.DataFrame(index = uniquePos)  # create empty viterbi dataframe
            # create first column of dataframe
            startCol = []
            wordsList = ['\n']
            for i in range(len(viterbi)):
                startCol.append((0,-1))
            startCol[-1] = (1,-1)
            viterbi[col] = startCol
        else:
            # add words into list
            wordsList.append(orig)
            addCol = []
            # iterate through each part of speech for the word
            for currentPos in range(len(viterbi)):
                addCol.append((0,-1))
                for checkPos in range(len(viterbi)):
                    # calculate necessary probabilities
                    probV = viterbi.iloc[checkPos,-1][0]
                    probM = markov.iloc[checkPos, currentPos]
                    # handle words that are out of vocabulary
                    if word not in uniqueWords:
                        probL = likelihood.loc['oov', uniquePos[currentPos]]
                    else:
                        probL = likelihood.loc[word, uniquePos[currentPos]]
                    prob = probV * probM * probL
                    # only keep max probability
                    if prob > addCol[-1][0]:
                        addCol[-1] = (prob, checkPos)  # NOTE: tuples key is (probability, part of speech)
            viterbi[col] = addCol  # add new column onto viterbi dataframe
