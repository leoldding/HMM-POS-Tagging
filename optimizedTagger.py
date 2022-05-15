#%% Likelihood and Transition Table

# create dictionaries 'tables' for likelihood and Markov
likelihood = {}
markov = {}

# initialize start part of speech for bigrams
prevpos = 'start'

# read training data file
with open('data/training.pos', 'r') as f:
    lines = f.readlines()
    for line in lines:
        # strip line to check if the line is empty (spacing between sentences)
        line = line.strip()
        if line != '':
            word = line.split("\t")[0].lower().strip()
            pos = line.split("\t")[1].lower().strip()

            # add word and part of speech pair into likelihood table
            if word not in likelihood:
                likelihood[word] = {}
            if pos not in likelihood[word]:
                likelihood[word][pos] = 1
            else:
                likelihood[word][pos] += 1

            # add part of speech pairs (bigrams) into Markov transition table
            if prevpos not in markov:
                markov[prevpos] = {}
            if pos not in markov[prevpos]:
                markov[prevpos][pos] = 1
            else:
                markov[prevpos][pos] += 1
            prevpos = pos
        else:
            # add 'start' placeholder part of speech into markov
            if prevpos not in markov:
                markov[prevpos] = {}
            if 'start' not in markov[prevpos]:
                markov[prevpos]['start'] = 1
            else:
                markov[prevpos]['start'] += 1
            prevpos = 'start'

#%% Probabilities

# convert likelihoods into probabilities
for word in likelihood.keys():
    count = sum(likelihood[word].values())
    for pos in likelihood[word].keys():
        likelihood[word][pos] /= count

# set an 'out of vocabulary' probability based on number of parts of speech
oovProb = 1/len(markov.keys())

# convert Markov transitions into probabilities
for firstpos in markov.keys():
    count = sum(markov[firstpos].values())
    for secondpos in markov[firstpos].keys():
        markov[firstpos][secondpos] /= count

#%% Tagging

# open output file to write to
output = open('output.txt', 'w')

# initialize sentence list
sentence = [('start', {'start': (1, 0)})]
# NOTE:
# each index in sentence is a tuple with output word at index 0 and dictionary at index 1
# dictionary at index 1 contains part of speech as keys and a tuple
# tuples in the dictionary have probability at index 0 and part of speech of previous word at index 1


with open('data/test.words', 'r') as input:
    words = input.readlines()
    for word in words:
        outWord = word.strip()  # keep a copy of non-lowercase word
        word = word.lower().strip()  # make lowercase word to use with likelihood and Markov transition tables
        # check if word is empty (end of sentence)
        if word != '':
            sentence.append((outWord, {}))  # add original word to sentence
            for prevpos in sentence[-2][1].keys():  # iterate through all parts of speech from previous word
                for pos in markov[prevpos].keys():  # iterate through all potential part of speech transitions
                    # set likelihood probability
                    if word in likelihood.keys() and pos in likelihood[word].keys():
                        probLikelihood = likelihood[word][pos]
                    else:
                        probLikelihood = oovProb
                    # set Markov transition probability
                    if pos in markov[prevpos].keys():
                        probTransition = markov[prevpos][pos]
                    else:
                        probTransition = 0
                    probViterbi = sentence[-2][1][prevpos][0] # set viterbi probability
                    probability = probLikelihood * probTransition * probViterbi # calculate total probability
                    if probability != 0:
                        if pos not in sentence[-1][1].keys() or probability > sentence[-1][1][pos][0]:
                            sentence[-1][1][pos] = (probability, prevpos)  # only keep maximum probabilities
        else:
            maxTuple = (0, 0)
            outputList = []
            # find the largest probability associated with the last word
            for key in sentence[-1][1].keys():
                if maxTuple[0] < sentence[-1][1][key][0]:
                    maxTuple = sentence[-1][1][key]
                    pos = key
            outputList.insert(0, (sentence[-1][0], pos))
            # iterate backwards through sentence list using maxTuple which holds probability and previous part of speech
            for index in range(len(sentence)-2, 0, -1):
                outputList.insert(0, (sentence[index][0], maxTuple[1]))
                maxTuple = sentence[index][1][maxTuple[1]]
            # write words and predicted part of speech into the output file
            for outputValues in outputList:
                output.write(outputValues[0] + '\t' + outputValues[1].upper() + '\n')
            output.write('\n')  # add newline between sentences
            sentence = [('start', {'start': (1, 0)})]

# close output file
output.close()
