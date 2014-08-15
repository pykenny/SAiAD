# -*- coding: UTF-8 -*-
import regex as re
from operator import attrgetter

class MiningGram:
    def __init__(self, g, A, B):
        self.gram = g
        
        self.freqA = sum(A)/len(A)
        self.freqB = sum(B)/len(B)

        self.occurA = sum(A)
        self.occurB = sum(B)
        
        if self.freqA > self.freqB:
            self.diff = (self.freqA + 0.002)/(self.freqB + 0.002)
        else:
            self.diff = (self.freqB + 0.002)/(self.freqA + 0.002)

def minetest(textname1, textname2):
    # CHECK PARAMETERS
    if type(textname1) != str or type(textname2) != str:
        print("Parameters should be str.")
        return
        
    # CHECK No.001 FILE's EXISTENCE
    try:
        fp = open("./Text/%s/001.txt" % (textname1), 'r', encoding='utf-8')
        fp.close()
        fp = open("./Text/%s/001.txt" % (textname2), 'r', encoding='utf-8')
        fp.close()
    except FileNotFoundError:
        print("File not found.")
        return

    # FORM FULL TEXT
    fulltext = ""
    text_1 = []
    text_2 = []
    
    chnum = 1
    while True:
        try:
            fp = open("./Text/%s/%03d.txt" % (textname1, chnum), 'r', encoding='utf-8')
            text_tmp = fp.read()
            text_1.append(text_tmp)
            fulltext = fulltext + text_tmp
            fp.close()
            chnum = chnum + 1
        except FileNotFoundError:
            break
    
    chnum = 1
    while True:
        try:
            fp = open("./Text/%s/%03d.txt" % (textname2, chnum), 'r', encoding='utf-8')
            text_tmp = fp.read()
            text_2.append(text_tmp)
            fulltext = fulltext + text_tmp
            fp.close()
            chnum = chnum + 1
        except FileNotFoundError:
            break

    # FORM UNIGRAM AND BIGRAM
    unigram = re.findall(r".", fulltext)
    unigram = [x for x in unigram if x.find('。') == -1]
    unigram = list(set(unigram))

    bigram = re.findall(r"..", fulltext, overlapped=True)
    bigram = [x for x in bigram if x.find('。') == -1]
    bigram = list(set(bigram))

    # MiningGram list for unigram and bigram
    mineugr = []
    minebgr = []

    occurtmp_1 = []
    occurtmp_2 = []

    for x in unigram:
        occurtmp_1.clear()
        occurtmp_2.clear()
        pattern = re.compile(x)

        for j in text_1:
            if pattern.search(j) == None:
                occurtmp_1.append(0)
            else:
                occurtmp_1.append(1)

        for j in text_2:
            if pattern.search(j) == None:
                occurtmp_2.append(0)
            else:
                occurtmp_2.append(1)
        mineugr.append(MiningGram(x, occurtmp_1, occurtmp_2))

    for x in bigram:
        occurtmp_1.clear()
        occurtmp_2.clear()
        pattern = re.compile(x)
        
        for j in text_1:
            if pattern.search(j) == None:
                occurtmp_1.append(0)
            else:
                occurtmp_1.append(1)

        for j in text_2:
            if pattern.search(j) == None:
                occurtmp_2.append(0)
            else:
                occurtmp_2.append(1)
        minebgr.append(MiningGram(x, occurtmp_1, occurtmp_2))

    # SORT UNIGRAM
    filename = "./Result/diff_unigram_%s_%s.txt" % (textname1, textname2)
    file = open(filename, "w", encoding="utf8")
    sort_tmp = sorted(mineugr, key=attrgetter('diff'), reverse=True)
    a = 1
    for x in sort_tmp:
        text_tmp = "%05d %s %02d %02d %.4f\n"%(a, x.gram, x.occurA, x.occurB, x.diff)
        file.write(text_tmp)
        a = a + 1
    file.close()
    
    print("Output result to %s..." % (filename))
    
    # SORT BIGRAM
    filename = "./Result/diff_bigram_%s_%s.txt" % (textname1, textname2)
    file = open(filename, "w", encoding="utf8")
    sort_tmp = sorted(minebgr, key=attrgetter('diff'), reverse=True)
    a = 1
    for x in sort_tmp:
        text_tmp = "%05d %s %02d %02d %.4f\n"%(a, x.gram, x.occurA, x.occurB, x.diff)
        file.write(text_tmp)
        a = a + 1
    file.close()

    print("Output result to %s..." % (filename))
    
    print("End module.")