# -*- coding: UTF-8 -*-
import regex as re
from math import log
from operator import attrgetter

# class GramRank:
class GramRank:
    def __init__(self, g, f, r = 0):
        self.gram = g
        self.freq = f
        self.rank = r

def yangtest(textname, chapters):
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

    unitnum = len(chapters)
    totalch = sum(chapters)
    
    unitpoint = []
    if unitnum == 1:
        unitpoint.append(totalch)
    else:
        for i in range(1, unitnum+1, 1):
            unitpoint.append(sum(chapters[0:i]))
    
    print("Read in fulltext...")
    # FORM FULL TEXT AND UNITS
    fulltext = ""
    unittext = []
    unittmp = ""
    for i in range(1, totalch+1, 1):
        fp = open("./Text/%s/%03d.txt" % (textname, i), 'r', encoding='utf-8')
        rtext = fp.read()
        fulltext = fulltext + rtext
        unittmp = unittmp + rtext
        if unitpoint.count(i) != 0:
            unittext.append(unittmp)
            unittmp = ""
        fp.close()
    
    # FORM UNIGRAM
    unigram = re.findall(r".", fulltext)
    unigram = [x for x in unigram if x.find('。') == -1]
    unigram = list(set(unigram))

    print("Unigram set formed. Total %d unigrams." % (len(unigram)))

    # CALCULATE RANK AND FREQUENCY IN EACH UNIT
    print("Calculating rank and frequency in each unit...")
    
    unitrank = []
    for x in unittext:
        rank_tmp = []
        for y in unigram:
            rank_tmp.append(GramRank(y, x.count(y)/len(x)))
        rank_tmp = sorted(rank_tmp, key=attrgetter('freq'), reverse=True)
        # Form Rank
        a = 1
        for i in range(0, len(rank_tmp), 1):
            if i == 0 or rank_tmp[i-1].freq > rank_tmp[i].freq:
                a = a + 1
                rank_tmp[i].rank = a
            else:
                rank_tmp[i].rank = a
        unitrank.append(rank_tmp)

    print("Rank and freqency calculated.")

    # CONSTRUCT FULL INFORMATION OF EACH GRAM
    gramlist = []
    for x in unigram:
        freq_tmp = []
        rank_tmp = []
        for y in range(0, len(unitrank), 1):
            gramdata = next(val for val in unitrank[y] if val.gram == x)
            freq_tmp.append(gramdata.freq)
            rank_tmp.append(gramdata.rank)
        gramlist.append(GramRank(x, freq_tmp, rank_tmp))
    
    unitrank.clear()
    print("Data integrated.")

    # FIND ALL UNIGRAM IN EVERY UNIT
    graminunit = []
    for x in unittext:
        gram_tmp = re.findall(r".", x)
        gram_tmp = [y for y in gram_tmp if y.find('。') == -1]
        gram_tmp = list(set(gram_tmp))
        graminunit.append(gram_tmp)
    print("All unigram in each unit found.")
    
    # CALCULATE DISTANCE
    dist = [[0.0 for i in range(unitnum)] for j in range(unitnum)]

    for x in range(0, unitnum, 1):
        for y in range(0, unitnum, 1):
            cotext = []
            factor = []
            rankdif = []
            if x >= y:
                continue
            else:
                cotext = [item for item in graminunit[x] if item in graminunit[y]]
                print("# of %d and %d 's co-gram: %d" % (x, y, len(cotext)))
                # Find every gram's:
                for z in cotext:
                    textdata = next(item for item in gramlist if item.gram == z)
                    # 1. Rank in each unit(GramRank.rank)
                    ch_rank = [textdata.rank[x], textdata.rank[y]]
                    # 2. Probability of occurence in each unit(GramRank.freq)
                    ch_freq = [textdata.freq[x], textdata.freq[y]]
                    # 3. Calculate F(w) and rank difference
                    factor.append(-(ch_freq[0]*log(ch_freq[0]))-(ch_freq[1]*log(ch_freq[1])))
                    rankdif.append(abs(ch_rank[0]-ch_rank[1]))
                # Calculate distance
                facsum = sum(factor)
                factor = [item/facsum for item in factor]
                for z in range(0, len(cotext), 1):
                    dist[x][y] = dist[x][y] + (rankdif[z]*factor[z])
                dist[x][y] = dist[x][y]/len(cotext)
    
    gramlist.clear()
    graminunit.clear()
    print("End distance calculation between each unit.")

    # PRINT OUT RESULT
    filename = "./Result/YangTestResult_%s.txt" % (textname)
    fp = open(filename, "w", encoding="utf-8")
    for x in range(0, unitnum, 1):
        for y in range(0, unitnum, 1):
            if x >= y:
                continue
            else:
                line_tmp = "%02d - %02d : %f\n" % (x, y, dist[x][y])
                fp.write(line_tmp)
    fp.close()
    print("Output to file %s. End module." % (filename))