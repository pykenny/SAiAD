# -*- coding: UTF-8 -*-
import regex as re
import numpy as np
from scipy import stats
from operator import attrgetter

class Gram:
    def __init__(self, g, f):
        self.gram = g
        self.freq = f
        self.gramfreq = []
        
    def addgramfreq(self, text, freqtype):
        if freqtype == 1:
            self.gramfreq.append(text.count(self.gram)/len(text))
        else:
            self.gramfreq.append(text.count(self.gram))

def t_test(c1, c2):
    group1 = np.array(c1)
    group2 = np.array(c2)
    
    # If no any occurence in both units, return 0.
    if sum(group1) == 0 and sum(group2) == 0:
        print("No Existence in both text.")
        return 0
    
    result = stats.ttest_ind(group1, group2)
    print("tval:%f prob:%f" % (result[0], result[1]))
    if result[1] < 0.005 or result[1] > 0.995:
        return 1
    else:
        return 0


def freqtest_occur(textname, chapters):
    # Check Parameters
    if type(textname) != str or len(textname) == 0:
        print("Parameter 'textname' should be a non-empty string.")
    if type(chapters) != list:
        print("Parameter 'chapters' should be list.")
        return
    for i in chapters:
        if type(i) != int:
            print("Values in list 'chapters' should be positive integers.")
        if i <= 0:
            print("Each unit should include at least one chapter.")
            return
            
    # Check Files
    try:
        for i in range(1, sum(chapters)+1, 1):
            fp = open("./Text/%s/%03d.txt" % (textname, i), 'r', encoding='utf-8')
            fp.close()
    except FileNotFoundError:
        print("Chapter NO.%03d does not exist!" % (i))
        return


    print("Searching top 100 unigrams...")

    unitnum = len(chapters)
    totalch = sum(chapters)

    # FORM FULL TEXT
    fulltext = ""
    for i in range(1, totalch+1, 1):
        fp = open("./Text/%s/%03d.txt" % (textname, i), 'r', encoding='utf-8')
        fulltext = fulltext + fp.read()
        fp.close()
    
    # FIND TOP 100 GRAMS WITH HIGHEST FREQUENCY
    gramlist = []
    unigram = re.findall(r".", fulltext)
    unigram = [x for x in unigram if x.find('。') == -1]
    unigram = list(set(unigram))

    for x in unigram:
        gramlist.append(Gram(x, fulltext.count(x)))
    gramlist = sorted(gramlist, key=attrgetter('freq'), reverse=True)
    gramlist = gramlist[0:100]

    print("Top 100 unigrams founded.")

    fp = open("./Result/unigram_freq100_%s.txt" % (textname), 'w', encoding='utf-8')
    for i in range(0, 100, 1):
        linetmp = "%03d %s %07d\n" % (i, gramlist[i].gram, gramlist[i].freq)
        fp.write(linetmp)
    fp.close()


    for i in range(1, totalch+1, 1):
        fp = open(fp = open("./Text/%s/%03d.txt" % (textname, i), 'r', encoding='utf-8'))
        chaptext = fp.read()
        chaptext.replace('。', '')
        for g in gramlist:
            g.addgramfreq(chaptext, 0)
        fp.close()

    print("End calculating unigram freq in each chapter.")

    # Group chapters and compare frequency
    res_out = [[0.0 for i in range(unitnum)] for j in range(unitnum)]

    for i in range(0, unitnum, 1):
        for j in range(0, unitnum, 1):
            if i >= j:
                continue
            diff = []
            st_i = sum(chapters[0:i])
            ed_i = sum(chapters[0:i+1])
            st_j = sum(chapters[0:j])
            ed_j = sum(chapters[0:j+1])
            for g in gramlist:
                diff.append(t_test(g.gramfreq[st_i:ed_i], g.gramfreq[st_j:ed_j]))
            res_out[i][j] = sum(diff)
            print("%d - %d: %f" % (i, j, res_out[i][j]))

    # Output Result
    filename = "./Result/freqdifference_byratio_%s.txt" % (textname)
    fp = open(filename, "w", encoding='utf-8')
    for i in range(0, unitnum, 1):
        for j in range(0, unitnum, 1):
            if i >= j:
                continue
            tmp_line = "%02d - %02d : %03d\n"%(i, j, res_out[i][j])
            fp.write(tmp_line)
    fp.close()
    print("Output to file %s. End module." % (filename))
    
def freqtest_ratio(textname, chapters):
    # Check Parameters
    if type(textname) != str or len(textname) == 0:
        print("Parameter 'textname' should be a non-empty string.")
    if type(chapters) != list:
        print("Parameter 'chapters' should be list.")
        return
    for i in chapters:
        if type(i) != int:
            print("Values in list 'chapters' should be positive integers.")
        if i <= 0:
            print("Each unit should include at least one chapter.")
            return
            
    # Check Files
    try:
        for i in range(1, sum(chapters)+1, 1):
            fp = open("./Text/%s/%03d.txt" % (textname, i), 'r', encoding='utf-8')
            fp.close()
    except FileNotFoundError:
        print("Chapter NO.%03d does not exist!" % (i))
        return


    print("Searching top 100 unigrams...")

    unitnum = len(chapters)
    totalch = sum(chapters)

    # FORM FULL TEXT
    fulltext = ""
    for i in range(1, totalch+1, 1):
        fp = open("./Text/%s/%03d.txt" % (textname, i), 'r', encoding='utf-8')
        fulltext = fulltext + fp.read()
        fp.close()
    
    # FIND TOP 100 GRAMS WITH HIGHEST FREQUENCY
    gramlist = []
    unigram = re.findall(r".", fulltext)
    unigram = [x for x in unigram if x.find('。') == -1]
    unigram = list(set(unigram))

    for x in unigram:
        gramlist.append(Gram(x, fulltext.count(x)))
    gramlist = sorted(gramlist, key=attrgetter('freq'), reverse=True)
    gramlist = gramlist[0:100]

    print("Top 100 unigrams founded.")

    fp = open("./Result/unigram_freq100_%s.txt" % (textname), 'w', encoding='utf-8')
    for i in range(0, 100, 1):
        linetmp = "%03d %s %07d\n" % ((i+1), gramlist[i].gram, gramlist[i].freq)
        fp.write(linetmp)
    fp.close()


    for i in range(1, totalch+1, 1):
        fp = open("./Text/%s/%03d.txt" % (textname, i), 'r', encoding='utf-8')
        chaptext = fp.read()
        chaptext.replace('。', '')
        for g in gramlist:
            g.addgramfreq(chaptext, 1)
        fp.close()

    print("End calculating unigram freq in each chapter.")

    # Group chapters and compare frequency
    res_out = [[0.0 for i in range(unitnum)] for j in range(unitnum)]

    for i in range(0, unitnum, 1):
        for j in range(0, unitnum, 1):
            if i >= j:
                continue
            diff = []
            st_i = sum(chapters[0:i])
            ed_i = sum(chapters[0:i+1])
            st_j = sum(chapters[0:j])
            ed_j = sum(chapters[0:j+1])
            for g in gramlist:
                diff.append(t_test(g.gramfreq[st_i:ed_i], g.gramfreq[st_j:ed_j]))
            res_out[i][j] = sum(diff)
            print("%d - %d: %f" % (i, j, res_out[i][j]))

    # Output Result
    filename = "./Result/freqdifference_byratio_%s.txt" % (textname)
    fp = open(filename, "w", encoding='utf-8')
    for i in range(0, unitnum, 1):
        for j in range(0, unitnum, 1):
            if i >= j:
                continue
            tmp_line = "%02d - %02d : %03d\n"%(i, j, res_out[i][j])
            fp.write(tmp_line)
    fp.close()
    print("Output to file %s. End module." % (filename))