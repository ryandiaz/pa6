import nltk
import random
from nltk.corpus import abc
from nltk.corpus import gutenberg
from nltk.corpus import genesis
from nltk.corpus import webtext

from nltk.probability import LidstoneProbDist  
from nltk.model import NgramModel 

def loadList(file_name):
    """Loads text files as lists of lines. Used in evaluation."""
    with open(file_name) as f:
        l = [line.strip() for line in f]
    return l

def decodeLine(lines):
    dict = {}
    for line in lines:
        translation = line.split(':')
        eng = translation[0]
        esp = translation[1].split(', ')
        dict[eng] = esp
    return dict


def trainModel():
    totalwords = abc.words() #+ genesis.words() + gutenberg.words() + webtext.words()
    estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
    BigramModel = NgramModel(2, totalwords)
    UnigramModel = NgramModel(1, totalwords)
    return (UnigramModel, BigramModel)


def main():
    """Tests the model on the command line. This won't be called in
        scoring, so if you change anything here it should only be code
        that you use in testing the behavior of the model."""

    dict_file = "./dict.txt"
    dictLines = loadList(dict_file)
    dict = decodeLine(dictLines)
    revDict = {}
    for key in dict:
        keyList = dict[key]
        for val in keyList:
            if val in revDict:
                revDict[val].append(key)
            else: 
                revDict[val] = [key]
    in_file = "./test_set.txt"
    doc = loadList(in_file)

    (UnigramModel, BigramModel) = trainModel()

    nouns = ['PRP', 'PRP$', 'NNP', 'NNPS', 'NNS', 'NN']
    adjectives = ['JJR', 'JJS', 'JJ']
    adverbs = ['RB', 'RBS', 'RBR']
    conjunctions = ['CC']
    verbs = ['VB','VBD','VBG','VBN','VBP','VBZ']


    for line in doc:
        print line
        punctuation = line[-1] 
        words = line.split()
        newWords = []
        spanWords = []
        for word in words:
            word = word.replace(".", "")
            word = word.replace(",", "")
            word = word.replace("?", "")
            word = word.replace("!", "")
            word = word.replace(";", "")
            word = word.replace(":", "")
            word = word.lower()
            spanWords.append(word)


        for tsize in range(4,1,-1):
            ilimit = len(spanWords) - tsize
            i = 0
            span1 = []
            
            while i < ilimit:
                phrase = ' '.join(spanWords[i:i+tsize])
                if(phrase in revDict):
                    span1.append(phrase)
                    i += tsize
                    continue
                span1.append(spanWords[i])
                i += 1

            span1 += spanWords[i:]
            spanWords = span1

        for word in spanWords:
            
            if word in revDict:
                nw = revDict[word][0]
                if len(revDict[word]) > 1:
                    maxW = ''
                    maxP = 0.0
                    if len(newWords) > 0:
                        
                        for ambW in revDict[word]:
                            
                            p = BigramModel.prob(ambW,[newWords[-1]])
                            
                            if p > maxP:
                                maxP = p
                                maxW = ambW
                    else:
                        for ambW in revDict[word]:

                            p = UnigramModel.prob(ambW,[])
                            if p > maxP:
                                p = maxP
                                maxW = ambW
                    nw = maxW 

                if len(nw.split()) > 1:
                    nws = nw.split()
                    for w in nws: 
                        newWords.append(w)
                        
                else:    
                    newWords.append(nw)
                
        newWords = filter(lambda a: a != '', newWords)
        posTags = nltk.pos_tag(newWords)
        reorderedWords = []
        # specific word reorderings
        i = 0
        while i < len(posTags) - 2:
            
            if i < len(posTags) - 2:
                if posTags[i][1] in nouns and posTags[i+1][1] in adverbs and posTags[i+2][1] in adjectives:
                    reorderedWords +=[posTags[i+2][0], posTags[i+1][0], posTags[i][0]]
                    i += 3
                    continue
                if posTags[i][1] in nouns and posTags[i+1][0] == 'of' and posTags[i+2][1] in adjectives:
                    reorderedWords += [posTags[i+2][0], posTags[i][0]]
                    i += 3
                    continue
                if posTags[i][0] == 'see' and posTags[i+1][1] in verbs and posTags[i+2][1] in nouns:
                    reorderedWords += [posTags[i+2][0], posTags[i+2][0], posTags[i+1][0]]
                    i+=3 
                    continue
            if i < len(posTags) - 3:
                if posTags[i][1] in nouns and posTags[i+1][1] in adjectives and posTags[i+2][1] in conjunctions and posTags[i+3][1] in adjectives:
                    reorderedWords += [posTags[i+1][0], posTags[i+2][0], posTags[i+3][0], posTags[i][0]]
                    i += 4
                    continue
            reorderedWords += [posTags[i][0]]
            i += 1

        reorderedWords += newWords[i:]

        newWords = reorderedWords
        reorderedWords = []             
        posTags = nltk.pos_tag(newWords)
        i = 0
        while i < len(posTags) - 1:
            if posTags[i][1] in nouns and posTags[i+1][1] in adjectives:
                reorderedWords += [posTags[i+1][0], posTags[i][0]]
                i += 2
                continue
            reorderedWords += [posTags[i][0]]      
            i += 1
 

        reorderedWords += newWords[i:]
        newWords = reorderedWords
        newWords = filter(lambda a: a != '', newWords)
        newSentence = ' '.join(newWords)
        newSentence = newSentence[0].upper() + newSentence[1:]
        newSentence.append(punctuation)
        print newSentence
        print '  ' 
        sentence = ""



if __name__ == '__main__':
    main()