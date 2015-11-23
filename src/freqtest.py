# -*- coding: UTF-8 -*-
import regex as re
import numpy as np
import time
from datetime import datetime
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

def t_test(c1, c2, pvalue):
    group1 = np.array(c1)
    group2 = np.array(c2)
    
    # If no any occurence in both units, return 0.
    if sum(group1) == 0 and sum(group2) == 0:
        print("No Existence in both text.")
        return 0
    
    result = stats.ttest_ind(group1, group2)
    print("tval:%f prob:%f" % (result[0], result[1]))
    if result[1] < (pvalue/2) or result[1] > (1.0 - (pvalue/2)):
        return 1
    else:
        return 0

def freqtest(textname, chapters, base, testamount = 100, pvalue = 0.01, start = 1, textencoding = 'utf-8'):
    freqbase = [0, 1]
    # Timestamp
    timestampstr = datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
    
    # Check Parameters
    if type(textname) != str or len(textname) == 0:
        print("Parameter 'textname' should be a non-empty string.")
        return
    if type(chapters) != list:
        print("Parameter 'chapters' should be a list.")
        return
    for i in chapters:
        if type(i) != int:
            print("Values in parameter 'chapters' should be positive integers.")
            return
        if i <= 0:
            print("Each unit in parameter 'chapters' should include at least one chapter.")
            return
    if base in freqbase == False:
        print("Parameter 'base' is invalid")
        return
    if type(testamount) != int or testamount < 1:
        print("Parameter 'testamount' should be a positive integer.")
        return
    if type(pvalue) != float or pvalue >= 0.5 or pvalue <= 0:
        print("Parameter 'pvalue' given is invalid. It should be among range (0, 0.5).")
        return
    if type(start) != int or start < 1:
        print("Parameter 'start' should be a positive integer.")
        return

    unitnum = len(chapters)
    totalch = sum(chapters)
    
    # Check Files
    print('Checking files...')
    try:
        for i in range(start, totalch+1, 1):
            fp = open("./Text/%s/%03d.txt" % (textname, i), 'r', encoding=textencoding)
            fp.close()
    except FileNotFoundError:
        print("Chapter NO.%03d does not exist!" % (i))
        return

    # Find the most frequent 100 unigrams in the text
    print("Searching top %d unigrams..." % (testamount))
    # Form full text
    fulltext = ""
    for i in range(start, totalch+1, 1):
        fp = open("./Text/%s/%03d.txt" % (textname, i), 'r', encoding=textencoding)
        fulltext = fulltext + fp.read()
        fp.close()
    # Form unigram list and sort by frequency
    gramlist = []
    unigram = re.findall(r".", fulltext)
    unigram = [x for x in unigram if x.find('。') == -1]
    unigram = list(set(unigram))

    for x in unigram:
        gramlist.append(Gram(x, fulltext.count(x)))
    gramlist = sorted(gramlist, key=attrgetter('freq'), reverse=True)
    gramlist = gramlist[0:testamount]

    fp = open("./Result/unigram_freq_%s_top%d_%s.txt" % (textname, testamount, timestampstr), 'w', encoding=textencoding)
    fp.write("%d - %d, %s\n" % (start, start + totalch - 1, str(chapters)))
    for i in range(0, testamount, 1):
        linetmp = "%03d %s %07d\n" % ((i+1), gramlist[i].gram, gramlist[i].freq)
        fp.write(linetmp)
    fp.close()
    
    print("Top unigrams found. The result is saved.")
    
    # Form each chapter's text
    print("Calculate unigram freq in each chapter...")
    for i in range(start, totalch+1, 1):
        fp = open("./Text/%s/%03d.txt" % (textname, i), 'r', encoding=textencoding)
        chaptext = fp.read()
        chaptext.replace('。', '')
        for g in gramlist:
            g.addgramfreq(chaptext, base)
        fp.close()

    # Group chapters into units and compare their frequency by 2-sample t-test
    print("Comparing each unit...")
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
                diff.append(t_test(g.gramfreq[st_i:ed_i], g.gramfreq[st_j:ed_j], pvalue))
            res_out[i][j] = sum(diff)
            print("%d - %d: %f" % (i, j, res_out[i][j]))

    # Output Result
    if base == 0:
        filename = "./Result/freqdifference_byoccur_%s_top%d_%s.txt" % (textname, testamount, timestampstr)
    elif base == 1:
        filename = "./Result/freqdifference_byratio_%s_top%d_%s.txt" % (textname, testamount, timestampstr)
    fp = open(filename, "w", encoding=textencoding)
    fp.write("%d - %d, %s\n" % (start, start + totalch - 1, str(chapters)))
    for i in range(0, unitnum, 1):
        for j in range(0, unitnum, 1):
            if i >= j:
                continue
            tmp_line = "%02d - %02d : %03d\n"%(i, j, res_out[i][j])
            fp.write(tmp_line)
    fp.close()
    print("Output to file %s. End module." % (filename))
    
# def freqtest_ratio(textname, chapters):
#     # Check Parameters
#     if type(textname) != str or len(textname) == 0:
#         print("Parameter 'textname' should be a non-empty string.")
#     if type(chapters) != list:
#         print("Parameter 'chapters' should be list.")
#         return
#     for i in chapters:
#         if type(i) != int:
#             print("Values in list 'chapters' should be positive integers.")
#         if i <= 0:
#             print("Each unit should include at least one chapter.")
#             return
#             
#     # Check Files
#     try:
#         for i in range(1, sum(chapters)+1, 1):
#             fp = open("./Text/%s/%03d.txt" % (textname, i), 'r', encoding='utf-8')
#             fp.close()
#     except FileNotFoundError:
#         print("Chapter NO.%03d does not exist!" % (i))
#         return
# 
# 
#     print("Searching top 100 unigrams...")
# 
#     unitnum = len(chapters)
#     totalch = sum(chapters)
# 
#     # FORM FULL TEXT
#     fulltext = ""
#     for i in range(1, totalch+1, 1):
#         fp = open("./Text/%s/%03d.txt" % (textname, i), 'r', encoding='utf-8')
#         fulltext = fulltext + fp.read()
#         fp.close()
#     
#     # FIND TOP 100 GRAMS WITH HIGHEST FREQUENCY
#     gramlist = []
#     unigram = re.findall(r".", fulltext)
#     unigram = [x for x in unigram if x.find('。') == -1]
#     unigram = list(set(unigram))
# 
#     for x in unigram:
#         gramlist.append(Gram(x, fulltext.count(x)))
#     gramlist = sorted(gramlist, key=attrgetter('freq'), reverse=True)
#     gramlist = gramlist[0:100]
# 
#     print("Top 100 unigrams founded.")
# 
#     fp = open("./Result/unigram_freq100_%s.txt" % (textname), 'w', encoding='utf-8')
#     for i in range(0, 100, 1):
#         linetmp = "%03d %s %07d\n" % ((i+1), gramlist[i].gram, gramlist[i].freq)
#         fp.write(linetmp)
#     fp.close()
# 
# 
#     for i in range(1, totalch+1, 1):
#         fp = open("./Text/%s/%03d.txt" % (textname, i), 'r', encoding='utf-8')
#         chaptext = fp.read()
#         chaptext.replace('。', '')
#         for g in gramlist:
#             g.addgramfreq(chaptext, 1)
#         fp.close()
# 
#     print("End calculating unigram freq in each chapter.")
# 
#     # Group chapters and compare frequency
#     res_out = [[0.0 for i in range(unitnum)] for j in range(unitnum)]
# 
#     for i in range(0, unitnum, 1):
#         for j in range(0, unitnum, 1):
#             if i >= j:
#                 continue
#             diff = []
#             st_i = sum(chapters[0:i])
#             ed_i = sum(chapters[0:i+1])
#             st_j = sum(chapters[0:j])
#             ed_j = sum(chapters[0:j+1])
#             for g in gramlist:
#                 diff.append(t_test(g.gramfreq[st_i:ed_i], g.gramfreq[st_j:ed_j]))
#             res_out[i][j] = sum(diff)
#             print("%d - %d: %f" % (i, j, res_out[i][j]))
# 
#     # Output Result
#     filename = "./Result/freqdifference_byratio_%s.txt" % (textname)
#     fp = open(filename, "w", encoding='utf-8')
#     for i in range(0, unitnum, 1):
#         for j in range(0, unitnum, 1):
#             if i >= j:
#                 continue
#             tmp_line = "%02d - %02d : %03d\n"%(i, j, res_out[i][j])
#             fp.write(tmp_line)
#     fp.close()
#     print("Output to file %s. End module." % (filename))