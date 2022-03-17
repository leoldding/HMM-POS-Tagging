#%% Importsimport numpy as npimport pandas as pdimport nltknltk.download('punkt')#%% Likelihood Table# create lists for words and parts of speechwords = []pos = []# read training file and add all words and parts of speech to respective listswith open('data/dev.pos', 'r') as f:    lines = f.readlines()    for line in lines:        line = line.strip()        if line != '':            words.append(line.split("\t")[0].lower().strip())            pos.append(line.split("\t")[1].lower().strip())        else:            pos.append('start')        # create a list of unique words and partrs of speechuniqueWords = sorted(set(words))uniquePos = sorted(set(pos))# put the 'start' part of speech at end uniquePos.remove('start')uniquePos.append('start')# create word to part of speech likelihood tablelikelihood = pd.DataFrame(index = uniqueWords, columns = uniquePos)# re-read training file but this time counting the amount of times a word in a part of speech occurswith open('data/dev.pos', 'r') as f:    lines = f.readlines()    for line in lines:        line = line.strip()        if line != '':            word = line.split('\t')[0].lower().strip()            part = line.split('\t')[1].lower().strip()            if pd.isnull(likelihood.loc[word,part]):                likelihood.loc[word,part] = 1            else:                likelihood.loc[word,part] += 1# go through each word normalizing its probability to add up to 1, mark nulls as 0for i in range(len(likelihood)):    count = np.nansum(likelihood.iloc[i])    for j in range(len(likelihood.iloc[i])):        if not pd.isnull(likelihood.iloc[i,j]):            likelihood.iloc[i,j] /= count        else:            likelihood.iloc[i,j] = 0            # create and add an 'out of vocabulary' row and add onto tableoov = np.full(len(likelihood.iloc[0]),1/len(likelihood.iloc[0]))likelihood.loc['oov'] = oov#%% Hidden Markov Model# create bigrams of parts of speech using nltkbigrams = list(nltk.bigrams(pos))# create markov matrix with unique parts of speechmarkov = pd.DataFrame(index = uniquePos, columns = uniquePos)# count pos transitions, except for transitioning to 'start'for current, transition in bigrams:    if transition != 'start':        if pd.isnull(markov.loc[current,transition]):            markov.loc[current, transition] = 1        else:            markov.loc[current,transition] += 1# normalize probabilities per row such that they add to 1for i in range(len(markov)):    count = np.nansum(markov.iloc[i])    for j in range(len(markov.iloc[i])):        if not pd.isnull(markov.iloc[i,j]):            markov.iloc[i,j] /= count        else:            markov.iloc[i,j] = 0        #%% POS Tagging# read in test setwith open('data/devtest.words', 'r') as f:    lines = f.readlines()    lines.insert(0,'\n')first = Truecol = 0for word in lines:    word = word.strip()    if word == '':        if not first:            #            break        first = False        startCol = np.full(len(uniquePos), 0)        startCol[-1] = 1        viterbi = pd.DataFrame(index = uniquePos)        viterbi[col] = startCol    else:        addCol = []        # iterate through each pos position        for i in range(len(viterbi)):            # if previous word pos probability is 0, add 0            if viterbi.iloc[i,len(viterbi.iloc[i])-1] == 0:                addCol.append(0)            else:                posArr = []                for i in range(len(markov.iloc[i])):                    pass                addCol.append(posArr)           viterbi[col] = addCol            col += 1