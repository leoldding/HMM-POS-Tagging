# HMM-POS-Tagging
Hidden Markov Model Part of Speech Tagging

## Work
Code for the tagging algorithm can be found in *optimizedTagger.py* and *tagger.py*.

## Goal 
Train an algorithm to tag words with different parts of speech based on prior probabilities and part of speech transition probabilities in a hidden Markov model.

## Data
Data comes from the Penn Treebank Corpus. The development files are from section 24; test file comes from section 23; training file is a compiled file of sections 2 to 21.

There are two different file extenions:

1) .pos

These files have two columns separated by a tab ('\t'). The first column is the word-token and the second column is the part of speech (POS) tag. A blank line ('/n') is used to separate sentences.

2) .words

These files only have one word-token per line with blanks between sentences.

## Outputs
The old *tagger.py* output is stored in *oldOutput.txt*.
The *optimizedTagger.py* output is stored in *output.txt*.

## Runtime
*tagger.py* completed its task in over 12 hours.
*optimizedTagger.py* completes its task in just over a minute.
*IMPORTANT TO GO BACK AND LOOK AT OLD CODE*

