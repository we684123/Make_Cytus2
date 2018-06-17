# Make_Cytus2
製作Cytus2譜面用；Make Cytus2 charts。    

基本上可以先用[Cytunity](http://cytus-fanon.wikia.com/wiki/User_blog:JCEXE/List_of_Cytus_simulation_programs:_2017_edition#Cytunity)對好時間跟位置後在輸出譜面並[將link跟時間重新綁好](https://cdn.discordapp.com/attachments/430987888042180610/431001210552582146/79e38aa80b706550.rar)後，再送來這邊做型態變換和變速。

First time you can use  [Cytunity](http://cytus-fanon.wikia.com/wiki/User_blog:JCEXE/List_of_Cytus_simulation_programs:_2017_edition#Cytunity) bind time and X axis position and hole time     
after , move chart to TPV4.9 , change speed and note type and output flie.       

if you understand the readme , and want to chang the English explanation , plz open issue or fork_push here .

---
## 怎麼使用Make_Cytus2 ； how to use Make_Cytus2
下載這個專案後開啟資料夾    

請將檔名 "XXX.hard.txt" 或 "XXX.easy.txt"(或是我提供的trytoc2.hard.txt) 複製到win64(依你的作業系統)資料內    
然後啟動 "Make_Cytus2.exe"    
之後產生3個檔案    
"XXX.v1plus" 可以複製內容至 Excel 監視內容    
"XXX.c2v0plus" 可以看詳細的轉換狀態    
"XXX.hard.txt.c2v0" 或 "XXX.easy.txt.c2v0" 則是 Cytus2_V0 格式的譜面檔。    

或者你是其他作業系統且有 Python3 則可以在同目錄中開啟命令視窗(cmd)輸入    
`python3 Make_Cytus2.py`    
//--------------------------------------------------------    
Download this repository and open folder    

plz copy file name "XXX.hard.txt" or "XXX.easy.txt" (or "trytoc2.hard.txt") to win64(or you are win32,mac) folder.    
and use "Make_Cytus2.exe" .    
after    
"XXX.v1plus" you can copy to Excel and click error.    
"XXX.c2v0plus" Cytus2_V0 flie details
"XXX.hard.txt.c2v0" or "XXX.easy.txt.c2v0" is Cytus2_V0 format flie .    

or if you computer OS is not Windows and have Python3,you can open Command window and run     
`python3 Make_Cytus2.py`

---
## Make_Cytus2格式 ; Make_Cytus2 format
採用自定義格式，不過是從V2格式上延伸過來的    
![Imgur](https://i.imgur.com/drpHot2.png)    

 - **VERSION 3**    
    //形式為整數 ， type=int    
    原本是用來宣告下方的譜面要用什麼方式使用，但現在沒用    
    just talk to charts player how to decord the chart file(in cytus)    
    But now it has no effect , so you can use 2 or 3 or more...    


 - **BPM 280**    
    //形式為整數 ， type=int    
    這一行在Cytus1V2中是控制譜面左右兩邊黑色區塊跳動的速度。    
    在Cytus2V0中則是設定最初的掃線速度。    
    you song how many beats in any 60 second    
    if you not understand plz see [BPM_wiki](https://en.wikipedia.org/wiki/Tempo)    


 - **PAGE_SHIFT 1.799999**    
    //形式為浮點數 ， type=float    
    掃線開始的位置，雖然在Cytus2上無法用，但在製作V2譜面就有用了    
    如果 PAGN_SIZE 設 0.8，PAGE_SHIFT 設0.2     
    那便換出現在Y軸的0.25處，且掃線方向向上(藍線)    
    (PAGE_SHIFT少於PAGN_SIZE向上，反之向下)    
    0.25 = 0.2 / 0.8    

    如果要粉線且向下呢?    
    PAGE_SHIFT = 0.8(PAGN_SIZE) + 0.2(0.25 * 0.8)    
    PAGE_SHIFT = 1.0    

    in cytus1_V2 chart format is decision scan line direction and position    

    if you set it to 0, the scan line will start in chart down(y=0)     
    and direction↑ (link to purple line)    

    if you PAGN_SIZE set to 0.8 and PAGE_SHIFT set to 0.2 , the scan line will start in chart down(y=0.25)     
    and direction↑ (link to blue line)    

    if you PAGN_SIZE set to 0.8 and PAGE_SHIFT set to 1.0 , the scan line will start in chart down(y=0.75) and     
    direction↓ (link to pink line)    
    ![Imgur](https://i.imgur.com/5lJSGkH.png)


 - **PAGE_SIZE 0.857142**    
    //形式為浮點數 ， type=float    
    掃線每掃一幕(or屏)所需要的時間    
    every chart use how much time (second)    
    EX：PAGE_SIZE 0.857142 = every page use 0.857142 second    


 - **scan_line_direction_opposite 1**    
    //形式為整數 ， type=int ； 只能輸入0或1 (only 0 or 1)    
    //預設為0 ， Default 0    
    掃線初始方向，一般來說為0，但如果實際方向相反的話可以調為1，他會再反過來。    
    the scan line direction is reverse direction ?     
    set "scan_line_direction_opposite 1" can reverse direction again    


 - **extension_of_time 0**    
    //形式為浮點數 ， type=float    
    //預設為0 ， Default 0    
    整體時間延遲或減少 如果為-3會全譜面的時間-3秒，4的話則全體+4秒    
    注意！如果你的 PAGE_SHIFT不等於0 或 不等於PAGN_SIZE的倍數(含一倍)    
    例如 PAGN_SIZE=0.8 然後 PAGE_SHIFT=1.6，那就不用用到這個，除非你原本的譜面時間就沒對準    

    然後如果不是是上述情況的話，extension_of_time的值會等於 PAGE_SHIFT%PAGN_SIZE(PAGE_SHIFT除PAGN_SIZE後取餘數)，這樣會把 PAGE_SHIFT 帶來的誤差修正回來。    

    if you aware you all note time is to fast or to late some time    
    if to fast 4 second , use extension_of_time -4 will be all note time -4 second    
    if to late 3 second , use extension_of_time 3 will be all note time 3 second    

    !!!    
    if you PAGE_SHIFT (not equal 0) or (equal PAGN_SIZE*n(n is Integer))    
    extension_of_time will equal (PAGE_SHIFT%PAGN_SIZE(PAGE_SHIFT MOD PAGN_SIZE))    


 - **auto_fix_type 0**    
    //形式為整數 ， type=int ； 只能輸入0或1 (only 0 or 1)    
    //預設為0 ， Default 0    
    自動幫忙修正HOLD溢出邊界的問題，但不保證效果，預期是如果你的HOLD長度小於該幕的總長且很接近邊界，這時後會自動把該HOLD移到下一幕中，如果是HOLD長度大於該幕的總長則會把note型態變成LONG    
    auto_fix_type just set 0 or 1 , if 0 will not auto fix chart error , 1 will auto fix     

    but it just auto fix HOLD error    
    if HOLD time over to PAGE_SIZE will set the note type to LONG    
    if HOLD time not over PAGE_SIZE and over to page boundary , it will move the note to next page    


 - **change_type_to_LONG_form_x**
 - **change_type_to_SLIDE_form_x**    
    //形式為三位數整數 或者0，type= Three-digit int or 0;
    //預設為0(不作用) ， Default 0 (if 0 = not work)   
    如果不想每次都手動換note type的話可以用這個，此會把符合設定的note x(X軸位置)值減去(設定值/1000000)，當作新的"x位置"，同時將該note的type轉為對應type。    
    這兩個 **設為0或不是3位整數時不作用!**。    
    The other methods can set note type to "SLIDE" or "LONG"    


    例如設定成 ; if you set like this    
    "change_type_to_LONG_form_x 123"    
    "change_type_to_SLIDE_form_x 456"    

    且有一個note為 ; and have a note    
    "NOTE 8 15.333210 0.500123 0.000000"    
    那麼因為他的x位置小數點後4位到後6位等於123，所以程式會把它當作    
    "LONG 8 15.333210 0.500000 0.000000" 去解讀。    
    (type變成LONG，x還原成 0.500000)    
    (type will reset "LONG"，x rerset 0.500000)    

    而如果有另一個note為 ; and have a note    
    "NOTE 9 15.833210 0.750456 0.000000"    
    因為0.750456的456，所以解讀成    
    "SLIDE 8 15.333210 0.750000 0.000000"    
    (type變成SLIDE，x還原成 0.750000)    
    (type will reset "SLIDE"，x rerset 0.750000)    

    **如果用此方式轉換的，請注意下列狀況!!!**    
    當你的note為下列狀況時，x(0.500123)並不會轉回(0.500000)    
    "SLIDE	5	10.499799	0.500123	0.000000"    

 - **format_version 0**    
    //形式為整數 ， type=int ；    
    //預設為0 ， Default 0    
    這是設定最後輸出譜面時的版本，基本上還是用0就好        
    now just set to 0 , if cytus2 chart format change ,maybe set to 1 ,just maybe    


 - **beat 4**    
    //形式為整數 ， type=int ；    
    //預設為4 ， Default 4    
    歌曲的節拍數，通常都是4拍，極少數情況是3拍    
    the song beat , usually is 4 , few is 3    


 - **time_base 480**    
    //形式為整數 ， type=int ；    
    //預設為480 ， Default 480    
    這個我也不太清楚，但知道設480就對了，估計跟一幕的"質量"有關    
    ma..... , I do not understand ..... , set it 480 (O    
    maybe about page "quality"   ┐(´д`)┌    


 - **conversion_constant 60000000**    
    //形式為整數 ， type=int ；    
    //預設為60000000 ， Default 60000000    
    這個是 秒數s 與 tick 換算關係的轉換常數，一般來說不用改，但如果你發現一開始note的時間是準的，到後面越來越不準，則可以細部微調，或者先試試改成 59999940 看看，不行那就自己在微調。    
    如果後面越來越快，稍微加一點，越慢則減少一點。    

    其公式為：
    BPM = 60000000 / value    
    C1_PAGE_SIZE =  60 * 歌曲拍結(beat) / BPM / 2    
    設歌曲拍結為4    
    C1_PAGE_SIZE =  60 * 4 / BPM / 2    
    設每屏(幕)tick數為 960    
    s/tick(每tick對應秒數) = C1_PAGE_SIZE / 設每屏(幕)tick    

    Conversion constant    
    how many second is how many tick    
    Conversion constant Default 60000000    

    if you 0\~10 note time is precise , but end note(if all note=445 , end note is 435\~445) not     
    you can reset conversion_constant     
    if end not time is to late , to add constant , to fast , to reduce constant .    

---    

**譜面範例**    

NOTE	0	9.642858	0.200000	0.000000    
SLIDE	1	9.642958	0.200000	0.000000    
LONG	2	10.071230	0.500000	0.500000    
HOLD	3	10.071430	0.800000	3.000000    
NOTE	4	10.071430	0.200000	0.000000    
CHC	1	10.071500    
BPM	560	10.273459557132    
NOTE	5	10.499799	0.500000	0.000000    
NOTE	6	11.499799	0.500000	0.754260    
LINK 4 5    

----
#### note的格式如下：    
(note型態)-(id)-(出現時間)-(出現時的x座標)-(持續時間)    
(字串string)-(整數int)-(浮點數float)-(浮點數float)-(浮點數float)    

**note型態(type)**：    
有 **NOTE、HOLD、LONG、SLIDE**    
分別是 點、長條、黃色超級長條、切    
然後 HOLD、LONG、SLIDE 是強制型態，可以用這個特性讓譜面更"繽紛"。    

另外 **完全兼容Cytus1_V2格式** ，如果你想用出 HOLD 也是可以用    
NOTE	6	11.499799	0.500000	0.754260    
這種方式是可以接受的。    
#### LINK 的格式如下：    
(LINK)-(目標id)-(目標id)-(目標id)....    
(字串string)-(整數int)-(整數int)-(整數int)...    

這個東西會將所選中的 note **強制轉成 LINK 型態！！！**，請務必注意此特性。    
(最高優先權)

if use LINK type the note will **forcibly reset type to NINK！！！**    
(The highest rule)

#### CHC 格式如下：    
(CHC)-(變速方式)-(作用時間)    
(字串string)-(整數int)-(浮點數float)    

如果要提示掃線速度變快，則可以用CHC達成    
變速方式 輸入  1 等於文字提示 "speed up"，且掃線顏色變 紅(R)    
變速方式 輸入 -1 等於文字提示 "speed down"，且掃線顏色變 綠(G)    
之後可能補上 0 變白色且沒文字    

CHC  1 will change scan color(R) and print "speed up"    
CHC -1 will change scan color(G) and print "speed down"    


#### BPM 格式如下：    
(BPM)-(欲變的BPM)-(作用時間)    
(字串string)-(整數int)-(浮點數float)    

欲變的BPM，如果一開始你的BPM是280，那你在此輸入560就等於兩倍快撥放。    

作用的時間只能是掃線到上下邊界的時間，可容許一點點的誤差，不要超過一幕掃線時間的8分之一為佳。    

此外 BPM作用時間 的部分可以用 TPV4.9 去自動生出來，請善加利用！    
(看 C12 跟 H10 ， 左上角資料要填(C2~C4)，列位不夠可以自己拉)    

if you want change scan line speed , you can use "BPM 560 10.273460"
scan line speed will start 10.273460 second change.

How to get scan_line_boundary_time?    
you can use TPV4.9 column H get this    
(see C12 and H10 ， Top left data(C2~C4) need to be fill)

![Imgur](https://i.imgur.com/aO3yNcm.png)

---
## 常見問題 Q&A

- 轉譜失敗?
  - 請依照 Make_Cytus2 的提示修正問題，如果沒提示那就繼續往下看吧。

  - 請檢察你的 note 時間是不是 **"不是由小到大"**，通常會有這樣問題的譜都是從 [Cytunity](http://cytus-fanon.wikia.com/wiki/User_blog:JCEXE/List_of_Cytus_simulation_programs:_2017_edition#Cytunity) 生出的譜，請點 "[將link跟時間重新綁好](https://cdn.discordapp.com/attachments/430987888042180610/431001210552582146/79e38aa80b706550.rar)" 並用該工具修好譜面後再把設定補上，之後才用 Make_Cytus2 來轉譜。
  - 請檢察你的譜面最上面13行設定是不是有照我方**規定順序排列**、有沒有按照格式規定去設置。    
  (例如 auto_fix_type 只能設0和1的整數，或是名稱跟值沒有空白分開，像是"beat4"(X) "beat 4"(O)，還是你輸入的空白不是空白，而是TAB鍵)
- Cytus2譜面撥放器?
  - 如何取得?    
    原主人還沒釋出，請自行想辦法。    
  - 按 start 後動了一下但沒有繼續播放?
    - 先試著把我給"trytoc2.hard.txt"轉譜面後播放看看，如果可以播放，那可能是你的譜面有問題，如果不能播放，先檢查你的"Settings.txt"文件設定是否正確，要是還是不行，那你可以用0.55版撥放器試試看，因為此程式在做的時候是用0.55版播放、驗證，若真的是撥放器的問題請找撥放器原作者QQ。
    - 如果是**經由Make_Cytus2轉換的**Cytus2的譜面有問題，那...你可以開個issue並附上譜面檔案和問題描述(細節越詳細越好)，或直接看是否是程式的問題，然後順手幫忙解決(###
- 這樣的製譜流程有點不順暢030...
  - 現在還沒有專屬製譜器就只能先這樣，雖然有打算做一個專屬製譜器，但課業繁重 短期內不可能了Orz。
  - 歡迎各位做一個CUI的Cytus2製譜器，我這專案已有提供部份數學公式(TPV and Make_Cytus2.py)，請自行取用。
- The English readme i do not understand...; 這英文翻譯不OK...    
  ...我盡力了... Orz...    
  歡迎提供更好的翻譯。    
  I tried my best to translate  Orz...    
  maybe you will do fix translate, if you do ,very thank you!    

---
## 版本資訊    
2018/06/17 -    
- 加入"檢查錯誤並PO出"、修復"get_new_page_list"、移除mac執行檔(有更新py2.7的Make_Cytus2)    
- eee錯誤次數未顯現，除錯架構可以在更好(之後看看怎麼改)    
