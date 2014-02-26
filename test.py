import nltk
import random

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
        #eng = line[0:line.index(":")]
        #esp = line[line.index(":")+1:]
        dict[eng] = esp
    return dict


#def tokenize(doc):
   # nltk.tokenize




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
  #          print val
            if val in revDict:
                revDict[val].append(key)
            else: 
                revDict[val] = [key]
 #   print revDict
    in_file = "./dev_set.txt"
    doc = loadList(in_file)

    nouns = ['PRP', 'PRP$', 'NNP', 'NNPS', 'NNS', 'NN']
    adjectives = ['JJR', 'JJS', 'JJ']
    adverbs = ['RB', 'RBS', 'RBR']
    conjunctions = ['CC']

    for line in doc:
        print line
        words = line.split()
        newWords = []
        spanWords = []
        for word in words:
            word = word.replace(".", "")
            word = word.replace(",", "")
            word = word.replace("?", "")
            word = word.replace("!", "")
            word = word.lower()
            spanWords.append(word)

        for tsize in range(2,4):
            for i in range(0, len(spanWords)-tsize+1, tsize ):
                phrase = ' '.join(spanWords[i:i+tsize])
                if(phrase in revDict):
                    spanWords[i] = phrase
                    newWords[i+1:i+tsize] = [""]*(tsize-1)

        for word in spanWords:
            if word in revDict:
                nw = revDict[word][0]
                if len(revDict[word]) > 1:
                    nw = random.choice(revDict[word])
                newWords.append(nw)
        posTags = nltk.pos_tag(newWords)
        # print posTags
        # print newWords
        # print 'diff in length= ', len(posTags) - len(newWords)
        for i in range(0, len(posTags) - 1):
            print i
            
            if i < len(posTags) - 2:
                if posTags[i][1] in nouns and posTags[i+1][1] in adverbs and posTags[i+2][1] in adjectives:
                    buf = newWords[i]
                    print posTags[i][0]
                    print newWords[i] 
                    # print 'deleting : ', buf
                    del newWords[i]
                    newWords.insert(i+2,buf)
                    # print 'inserted at ', i+2

            if i < len(posTags) - 3:
                if posTags[i][1] in nouns and posTags[i+1][1] in adjectives and posTags[i+2][1] in conjunctions and posTags[i+3][1] in adjectives:
                    buf = newWords[i]
                    print posTags[i][0]
                    print newWords[i]
                    # print 'deleting: ', buf
                    del newWords[i]
                    newWords.insert(i+3,buf)
                    # print 'inserted at ', i+3
        posTags = nltk.pos_tag(newWords)
                   
        for i in range(len(posTags)-1):
            if posTags[i][1] in nouns and posTags[i+1][1] in adjectives:
                buf = newWords[i]
                newWords[i] = newWords[i+1]
                newWords[i+1] = buf        
 

            # else:
            #     newWords.append("nothing_yet")
        print ' '.join(newWords)
        print '  ' 
        sentence = ""
  #      for word in newWords:
   #         sentence = sentence + word + " "
    #    print sentence



    #docTokenized = tokenize(doc)



if __name__ == '__main__':
    main()