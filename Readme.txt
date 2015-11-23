# 2015/11/23 Functions in this package is under adjustment,
#            So some descriptions in this file are obsolete.

*************************************************************
2014 Spring Project -- Stylish Analysis in Authorship Dispute
README
		                             B98703010 謝博宇
		                                   2014/08/03
*************************************************************


一。開發環境

    在python3.4.1下開發。
　　使用上需要安裝python，並安裝SciPy，NumPy，regex三個library。
　　SciPy and NumPy: http://www.scipy.org/
　　regex: https://pypi.python.org/pypi/regex

二。前置工作／文本處理

　　(1)前置
　　   在你想處理文本的路徑下放入src資料夾，並加入兩個"Text"與"Result"的資料夾。
　　　 src下應含有以下.py檔：
       __init__.py  depunch.py  freqtest.py  minetest.py  textsearch.py  yangtest.py
　　　 要使用特定模組時，在處理文本的路徑下輸入：
       >> from src import (模組名稱)
　　　 例：使用freqtest模組，輸入：
       >> from src import freqtest
    
　　(2)加入新文本
       請使用UTF-8作為文本的編碼。
　　　 將文本的每個章節(或是分切的每個單位)以個別的txt檔儲存，檔名為「(章節編號).txt」。第一篇的章節編號為1。(章節編號的最大值為999)
　　　 例：欲處理的文本被分切成8個章節，則8個檔案的檔名依序是：
　　　 1.txt  2.txt  3.txt  4.txt  5.txt  6.txt  7.txt  8.txt
　　　 
　　　 文檔內的第一行請輸入標題，第二行後為文本內容，用於後述的標點處理。
　　　 例：
       ----檔案起始----
       第一回  甄士隱夢幻識通靈 賈雨村風塵懷閨秀　　　　　　<-- 這段在標點處理時不會被收入
       此開卷第一回也。作者自云...                          <-- 會收入到內文
       ......(其他內文)......                               <-- 會收入到內文　　　　　　　　　　　　　 
       ...不知有何禍事，且聽下回分解。　　　　　　　　　　　<-- 會收入到內文
       ----檔案結束----
　　　 
　　　 將章節檔案放在一個資料夾中，資料夾以文本的名稱命名。
　　　 例：上述的文本名稱如果要命名為「我的文本」，則建立一個名稱為「我的文本」資料夾，並把8個文字檔放在該資料夾下。

　　　 最後將新文本的資料夾加入"Text"資料夾。

　　(3)標點處理
　　　 加入新文本後，使用depunch模組中的depunchtext函式來處理，
　　　 將所有非中文字(包含標點符號)的內容刪除，並以句號取代之。
　　　 處理過的各章節檔案會存在同一個資料夾中，名稱以三位整數表示。
　　　 例：將「我的文本」中的8個檔案進行標點處理，則輸入：
　　　 >> from src import depunch
       >> depunch.depunchtext("我的文本")
　　　 處理後「我的文本」資料夾中會多出以下檔案：
　　　 001.txt  002.txt  003.txt  004.txt  005.txt  006.txt  007.txt  008.txt
　　　 於此，「我的文本」的內容已經處理完畢，可以使用於各個分析工具。

三。模組

　　(1)yangtest.py
　　　 yangtest(textname, chapters)　對文本做Rank-Frequency Distance分析。
　　　   ＃Parameters
　　　　　 textname(str): 文本名稱。
           chapters(list): 分切文本的方式。list中各項依序為每個分析單元的章節數。
　　　　 ＃Output
           結果會輸出到「Result」資料夾。檔名為「YangTestResult_(textname).txt」
　　　　　 檔案內各行為每個單元互相比較的結果：
　　　　　 (單元1) - (單元2): (Distance)
         ＃Example
　　　　   如果要將「我的文本」的8章以每2章做為一個單位進行分析，則輸入：
　　　　　 >> from src import yangtest as yt
           >> yt.yangtest("我的文本", [2, 2, 2, 2])
　　　　 　「Result」資料夾下會增加「YangTestResult_我的文本.txt」這個檔案。

　　(2)freqtest.py
　　　 freqtest_occur(textname, chapters)　對文本做前100字在各章出現次數平均的t-test。
　　　   ＃Parameters
　　　　　 textname(str): 文本名稱。
           chapters(list): 分切文本的方式。list中各項依序為每個分析單元的章節數。
　　　　 ＃Output
　　　　　 前100字的內容和比較結果會輸出到「Result」資料夾。
　　　　　 前100字的檔名為「unigram_freq100_(textname).txt」
           比較結果的檔名為「freqdifference_byoccur_(textname).txt」
　　　　　 檔案內各行為每個單元互相比較的結果：
　　　　　 (單元1) - (單元2): (# of difference)
         ＃Example
　　　　   如果要將「我的文本」的8章以每2章做為一個單位進行分析，則輸入：
　　　　　 >> from src import freqtest as ft
           >> ft.freqtest_occur("我的文本", [2, 2, 2, 2])
　　　　 　「Result」資料夾下會增加「unigram_freq100_我的文本.txt」、「freqdifference_byoccur_我的文本.txt」這兩個檔案。

　　　 freqtest_ratio(textname, chapters)　對文本做前100字在各章出現比率平均的t-test。
　　　   ＃Parameters
　　　　　 textname(str): 文本名稱。
           chapters(list): 分切文本的方式。list中各項依序為每個分析單元的章節數。
　　　　 ＃Output
　　　　　 前100字的內容和比較結果會輸出到「Result」資料夾。
　　　　　 前100字的檔名為「unigram_freq100_(textname).txt」
           比較結果的檔名為「freqdifference_byratio_(textname).txt」
　　　　　 檔案內各行為每個單元互相比較的結果：
　　　　　 (單元1) - (單元2): (# of difference)
         ＃Example
　　　　   如果要將「我的文本」的8章以每2章做為一個單位進行分析，則輸入：
　　　　　 >> from src import freqtest as ft
           >> ft.freqtest_ratio("我的文本", [2, 2, 2, 2])
　　　　 　「Result」資料夾下會增加「unigram_freq100_我的文本.txt」、「freqdifference_byratio_我的文本.txt」這兩個檔案。

　　(3)minetest.py
　　　 minetest(textname1, textname2)　對兩份文本進行單字與雙字詞的文字採礦分析。
　　　   ＃Parameters
　　　　　 textname1(str): 文本1的名稱。
           textname2(str): 文本2的名稱。
　　　　 ＃Output
           結果會輸出到「Result」資料夾。檔名為「diff_unigram_(textname1)_(textname2).txt」與「diff_bigram_(textname1)_(textname2).txt」。
　　　　　 檔案內各行為排序過的單/雙字詞：
　　　　　 (Rank) (Gram) (At) (Bt) (ft)
         ＃Example
　　　　   如果要將「我的文本1」和「我的文本2」進行分析，則輸入：
　　　　　 >> from src import minetest as mt
           >> mt.minetest("我的文本1", "我的文本2")
　　　　 　「Result」資料夾下會增加「diff_unigram_我的文本1_我的文本2.txt」和「diff_bigram_我的文本1_我的文本2.txt」這兩個檔案。

　　(4)textsearch.py
　　　 findaffix(textname, gram, isprefix, length)　對文本進行綴詞分析。
　　　   ＃Parameters
　　　　　 textname(str): 文本的名稱。
           gram(str): 搜尋綴詞的目標字詞。
　　　　　 isprefix(bool): True為搜尋前綴詞，False為搜尋後綴詞。
           length(int): 綴詞長度。為大於0的值。
　　　　 ＃Output
           結果會輸出到「Result」資料夾。檔名為「affix_(textname)_(gram)_pre(length).txt」(前綴詞)
           或「affix_(textname)_(gram)_post(length).txt」(後綴詞)。
　　　　　 檔案內各行為排序過的綴詞：
　　　　　 (綴詞) (# of occurence)
         ＃Example
　　　　   如果要尋找「我的文本」中「了」的『前一字』綴詞，則輸入：
　　　　　 >> from src import textsearch as ts
           >> ts.findaffix("我的文本", "了", True, 1)
　　　　 　「Result」資料夾下會增加「affix_我的文本_了_pre1.txt」這個檔案。

　　   findsentence(gram, textname)　尋找文本中特定字詞出現的單句。
　　　   ＃Parameters
           gram(str): 目標字詞。
　　　　　 textname(str): 文本的名稱。
　　　　 ＃Output
           結果會輸出到「Result」資料夾。檔名為「findsentence_(textname)_(gram).txt」
　　　　　 檔案內各行為找出的單句：
　　　　　 (# of chapter) (sentence)
         ＃Example
　　　　   如果要尋找「我的文本」中含有「看了」的單句，則輸入：
　　　　　 >> from src import textsearch as ts
           >> ts.findsentence("看了", "我的文本")
　　　　 　「Result」資料夾下會增加「findsentence_我的文本_看了.txt」這個檔案。

四。Information

　　(1)Version
       - Ver 1.00 (2014/08/03)

　　(2)Contact 
       Email: b98703010@ntu.edu.tw / pykenny@gmail.com
