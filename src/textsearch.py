# -*- coding: UTF-8 -*-
import regex as re
import time
from datetime import datetime

def affix(gram, text, isprefix, length):
    if isprefix == True:
        pattern = re.compile('.' * length + gram)
    else:
        pattern = re.compile(gram + '.' * length)
    
    result_all = re.findall(pattern, text, overlapped=True)
    result_all = [i for i in result_all if i.find('。') == -1]
    result_uni = list(set(result_all))
    
    result = []
    
    for i in result_uni:
        dic_tmp = {}
        dic_tmp['gram'] = i
        dic_tmp['freq'] = result_all.count(i)
        result.append(dic_tmp)
        
    result = sorted(result, key=lambda k: k['freq'], reverse=True)
        
    return result

def findgram(gram, text):
    result = [x for x in text.split('。') if x.find(gram) != -1]
    return result

def findaffix(textname, gram, isprefix, length):
    timestampstr = datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
    
    # CHECK PARAMETERS
    if type(textname) != str or type(gram) != str or type(isprefix) != bool or type(length) != int:
        print("Wrong type in parameters!")
        return
    
    if length <= 0:
        print("Parameter length should be positive integer.")
        return
    try:
        fp = open("./Text/%s/001.txt" % (textname), 'r', encoding='utf=16')
        fp.close()
    except FileNotFoundError:
        print("File not found!")
        return
    
    fulltext = ""    
    ch = 1
    while True:
        try:
            filename = "./Text/%s/%03d.txt" % (textname, ch)
            fp = open(filename, 'r', encoding='utf-8')
            fulltext = fulltext + fp.read()
            fp.close()
            ch = ch + 1
        except FileNotFoundError:
            break
    
    print("Searching %s..." % (textname))
    result = affix(gram, fulltext, isprefix, length)

    if isprefix == True:
        filename = "./Result/affix_%s_%s_pre%d_%s.txt" % (textname, gram, length, timestampstr)
    else:
        filename = "./Result/affix_%s_%s_post%d_%s.txt" % (textname, gram, length, timestampstr)
    print("Output result to %s..." % (filename))
    fp = open(filename, 'w')
    for i in result:
        linetmp = "%s %07d\n" % (i['gram'], i['freq'])
        fp.write(linetmp)
    fp.close()
    print("Done!")
    
def findsentence(gram, textname):
    timestampstr = datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
    # CHECK PARAMETERS
    if type(gram) != str or type(textname) != str:
        print("Parameters should be type str.")
        return
    try:
        fp = open("./Text/%s/001.txt" % (textname), 'r', encoding='utf-8')
        fp.close()
    except FileNotFoundError:
        print("File not found!")
        return
    
    chaptext = []
    result = []
    
    # FORM CHAPTER TEXT
    ch = 1
    while True:
        try:
            fp = open("./Text/%s/%03d.txt" % (textname, ch), 'r', encoding='utf-8')
            chaptext.append(fp.read())
            fp.close()
            ch = ch + 1
        except FileNotFoundError:
            break
    
    for i in range(0, len(chaptext), 1):
        print("Search: Chapter %03d..." % (i + 1))
        result.append(findgram(gram, chaptext[i]))

    filename = "./Result/findsentence_%s_%s_%s.txt" % (textname, gram, timestampstr)
    fp = open(filename, 'w', encoding='utf-8')
    for i in range(0, len(result), 1):
        if len(result[i]) == 0:
            fp.write("No occurence in chapter %03d.\n" % (i+1))
        else:
            for j in range(0, len(result[i]), 1):
                fp.write("%03d %s\n" % (i+1, result[i][j]))
    fp.close()
    
    print("Save to file %s. Done!" % (filename))