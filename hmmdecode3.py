import sys
import copy
from math import log
import time

def inputProcessing():
    modelfile = open("hmmmodel.txt", "r", encoding="utf8")
    wordCount = int(modelfile.readline().strip())
    uniquewords = modelfile.readline().split(' ')
    tags = modelfile.readline().split(' ')
    tagCount = {}
    line = modelfile.readline()
    while line != '\n':
        tagandcount = line.rsplit(' ', 1)
        tagCount[tagandcount[0]] = tagandcount[1].strip()
        line = modelfile.readline()

    tagListofWord={}
    line = modelfile.readline()
    while line != '\n':
        worditstags = line.split(' ')
        w=worditstags[0]
        tagListofWord[w] = worditstags[1:]
        line = modelfile.readline()

    wordTagProb = {}
    line = modelfile.readline()
    while line != '\n':
        wordTagP = line.rsplit(':', 1)
        wordTagProb[wordTagP[0]] = wordTagP[1].strip()
        line = modelfile.readline()

    tagTagProb = {}
    line = modelfile.readline()
    while line != '\n':
        tagTagP = line.rsplit(':', 1)
        tagTagProb[tagTagP[0]] = tagTagP[1].strip()
        line = modelfile.readline()

    oneCount = {}
    line = modelfile.readline()
    while line != '':
        tc = line.rsplit(' ', 1)
        oneCount[tc[0]] = tc[1].strip()
        line = modelfile.readline()

    return wordCount,uniquewords,tagCount,tags,tagListofWord,wordTagProb,tagTagProb,oneCount

def main(untaggedFile):
    totalnoofwords, vocab, tagCount, tags, tagListofWord, wordTagProb, tagTagProb, oneCount=inputProcessing()
    totaltags=len(tags)
    outFile = open("hmmoutput.txt", "w", newline='', encoding="utf8")
    rawFile = open(untaggedFile, "r", encoding="utf8")
    lines = rawFile.readlines()
    for line in lines:
        words = line.split(' ')
        backptr = {}
        probmatrix = {}
        prevleveltag = set()
        prevleveltag.add('ST')
        probmatrix['ST'] = 0

        maxkey = ''  # tag with maximum probability for last word of the sentence
        for i in range(0, len(words)+1):
            if i<len(words):
                word = words[i].strip()
                leveltags = tagListofWord.get(word, tags[:])
            else:
                leveltags = ['END']
                word = ''
            prevword = words[i - 1].strip()
            if i == 0:
                backkeyhalf = ''
            else:
                backkeyhalf = str(i - 1) + ' ' + prevword + '/'
            for tag in leveltags:
                maxprobviterbi = -999999
                tag = tag.strip()
                key = str(i) + ' ' + word + '/' + tag
                for prevtag in prevleveltag:  # going from all tag t-1 to tag t
                    prevtag=prevtag.strip()
                    wordkey = (word + '/' + tag)
                    orvalue=int(oneCount[tag])/int(tagCount[tag])
                    #print(orvalue)
                    wordtagprob = float(wordTagProb.get(wordkey,log(orvalue)))

                    tagkey = (prevtag + '/' + tag)
                    tagtagprob = float(tagTagProb[tagkey])

                    backkey = backkeyhalf+prevtag
                    probmatrix[key] = probmatrix[backkey] + tagtagprob + wordtagprob

                    if maxprobviterbi < probmatrix[key]:
                        maxprobviterbi = probmatrix[key]
                        maxkey = key
                        backptr[key] = backkey

            prevleveltag = leveltags[:] #l-1 tags for level l
        decodesequence = []
        maxkey = backptr[maxkey]#This will pop out backpointer of 'n END'
        while maxkey != 'ST':
            # tagonly = maxkey.split(' ')
            decodesequence.append(maxkey.split(' ')[1])
            maxkey = backptr[maxkey]

        lasttag=decodesequence[0]
        printseq=decodesequence[::-1]
        for wordbartag in printseq[:-1]:
            outFile.write(wordbartag+' ')
        outFile.write(lasttag)
        outFile.write('\n')


if __name__=="__main__":
    # print(time.time())
    main("en_dev_raw.txt")
    #main(sys.argv[1])
    # print(time.time())