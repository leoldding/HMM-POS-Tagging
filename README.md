# HMM-POS-Tagging
Hidden Markov Model Part of Speech Tagging

## Work
Code for the tagging algorithm can be found in 'tagger.py'.

## Goal 
Train an algorithm to tag words with different parts of speech based on prior probabilities and part of speech transition probabilities in a hidden markov model.

## Data
Data comes from the Penn Treebank Corpus. The development files are from section 24; test file comes from section 23; training file is a compiled file of sections 2 to 21.

There are two different file extenions:

1) .pos

These files have two columns separated by a tab ('\t'). The first column is the word-token and the second column is the part of speech (POS) tag. A blank line ('/n') is used to separate sentences.

2) .words

These files only have one word-token per line with blanks between sentences.




