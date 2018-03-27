# number of unique words
# number of unique tags
# word given tag probabilities
# tag given previous tag probabilities
# frequency of every tag
# import time
import sys
from math import log


def main(trainingFile):
    tags = set()
    tagstr = ''
    words = set()
    uniquewordsstr=''
    wordTags = {}  # [word][tag] frequency
    tagPrevTag = {}  # [tag-1][tag] frequency
    enDev = open(trainingFile, "r", encoding="utf-8")
    lines = enDev.readlines()
    tagCount = {}  # frequency of all tags
    tagCount['ST'] = len(lines)
    tagCount['END'] = len(lines)

    f = open("hmmmodel.txt", "w", newline="", encoding="utf-8")
    tagsofword={}
    for line in lines:

        line.strip()  # strip of \n at the end of each line
        pairs = line.split(' ')  # word/tag pairs
        prev = 'ST'  # start tag for every sentence
        for i in range(0, len(pairs)):
            wt = pairs[i].rsplit('/', 1)
            word = wt[0].replace('\n', '')
            tag = wt[1].replace('\n', '')
            # getting all the unique tags and all the unique words
            if tag not in tags:
                tagstr += tag + ' '
            if word not in words:
                uniquewordsstr+=word+' '
                tagsofword[word]=''
            tags.add(tag)
            words.add(word)

            if tag not in tagCount:
                tagCount[tag] = 1
            else:
                tagCount[tag] += 1

            # word|tag count and tag|tag-1 count
            wordtag = word + '/' + tag
            if wordtag not in wordTags:
                wordTags[wordtag] = 1
                tagsofword[word]+=tag+' '
            else:
                wordTags[wordtag] += 1

            tagtag = prev + '/' + tag  # (t-1|t)
            prev = tag
            if tagtag not in tagPrevTag:
                tagPrevTag[tagtag] = 1
            else:
                tagPrevTag[tagtag] += 1

        tagtag = prev + '/' + 'END'
        if tagtag not in tagPrevTag:
            tagPrevTag[tagtag] = 1
        else:
            tagPrevTag[tagtag] += 1

    uniquewords = len(words)
    f.write(str(uniquewords))
    f.write('\n')
    f.write(uniquewordsstr.strip())
    f.write('\n')
    f.write(tagstr.strip())
    f.write('\n')

    onecountwt={}
    for tag, tagcount in tagCount.items():
        onecountwt[tag]=0
        f.write(tag + ' ' + str(tagcount))
        f.write('\n')

    f.write('\n')
    for word,itstags in tagsofword.items():
        f.write(word+' '+itstags.strip())
        f.write('\n')

    f.write('\n')
    wordTagProb = {}
    totaltags = len(tags)
    for wordtag, count in wordTags.items():
        wordandtag = wordtag.rsplit('/', 1)
        tag = wordandtag[1]
        wordTagProb[wordtag] = log(count/tagCount[tag])
        f.write(wordtag.strip() + ":" + str(wordTagProb[wordtag]))
        if count==1:
            onecountwt[tag]+=1
        f.write('\n')

    f.write('\n')
    tags.add('ST')
    tags.add('END')
    for tag in tags:
        for prevtag in tags:
            transition = prevtag + '/' + tag
            if transition not in tagPrevTag:
                tagPrevTag[transition]=0

    tagTagProb = {}
    for tagtag, count in tagPrevTag.items():
        prevtag = tagtag.rsplit('/', 1)[0]
        tagTagProb[tagtag] = log((count+1) / (tagCount[prevtag]+totaltags))  # (t-1|t)/t-1
        f.write(tagtag.strip() + ":" + str(tagTagProb[tagtag]))
        f.write('\n')

    f.write('\n')
    for tag, onecount in onecountwt.items():
        f.write(tag + ' ' + str(onecount+1))
        f.write('\n')


if __name__=="__main__":
    #print(time.time())
    # main(sys.argv[1])
    main("en_train_tagged.txt")
    #print(time.time())