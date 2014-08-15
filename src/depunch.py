# -*- coding: utf-8 -*-
import regex as re

class Text:
    def __init__(title, text):
        self.title = title
        self.text = text

def depunch(cdata, text):
    splitted = re.findall(cdata, text)
    newtext = ""
    for i in splitted:
        newtext = newtext + i + "。"
    return newtext


def depunchtext(textname):
    try:
        fp = open("./Text/%s/1.txt" % (textname), 'r', encoding='utf-8')
    except FileNotFoundError:
        print("Text folder does not exist, or documents do not start from 1.txt")
        return
        
    CDATA = re.compile(u'[⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]+', re.UNICODE)
    tit = ""
    txt = ""
    txtcount = 1
    
    while True:
        try:
            titleflag = 0
            txt = ""            
            filedir = "./Text/%s/%d.txt" % (textname, txtcount)
            for line in open(filedir, 'r', encoding='utf16'):
                if titleflag == 0:
                    tit = line
                    titleflag = 1
                else:
                    line = depunch(CDATA, line + '。')
                    txt = txt + line
            # Write to new file
            filedir = "./Text/%s/%03d.txt" % (textname, txtcount)
            fp = open(filedir, 'w', encoding='utf16')
            fp.write(txt)
            fp.close()
            txtcount = txtcount + 1
        except FileNotFoundError:
            print("End depunch of %s." % (textname))
            break
        else:
            continue