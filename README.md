# Make_Cytus2
製作Cytus2譜面用；Make Cytus2 charts。    

基本上可以先用[Cytunity](http://cytus-fanon.wikia.com/wiki/User_blog:JCEXE/List_of_Cytus_simulation_programs:_2017_edition#Cytunity)對好時間跟位置後在輸出譜面並[將link重新綁好](https://cdn.discordapp.com/attachments/430987888042180610/431001210552582146/79e38aa80b706550.rar)後，再送來這邊作型態變換和變速。

---
## 怎麼使用 how to use
下載這個專案後開啟資料夾

請將檔名 "XXX.hard.txt" 或 "XXX.easy.txt" 複製到win64資料內
然後啟動 "Make_Cytus2.exe"
之後產生兩個檔案
"XXX.v1plus" 可以複製內容至 Excel 監視內容
"XXX.hard.txt.c2v0" 或 "XXX.easy.txt.c2v0" 則是 Cytus2_V0 格式的譜面檔。

或者你是其他作業系統且有 Python3 則可以在同目錄中開啟命令視窗(cmd)輸入
`python3 Make_Cytus2.py`
//--------------------------------------------------------
Download this repository and open folder

plz copy file name "XXX.hard.txt" or "XXX.easy.txt" to win64 folder.
and use "Make_Cytus2.exe" .
after
"XXX.v1plus" you can copy to Excel and click .
"XXX.hard.txt.c2v0" or "XXX.easy.txt.c2v0" is Cytus2_V0 format flie .

or if you computer OS is not Windows and have Python3,you can open Command window and run 
`python3 Make_Cytus2.py`

---
## 格式
採用自定義格式，不過是從V2格式上延伸過來的    
![Imgur](https://i.imgur.com/5VCx1VR.png)    

**VERSION 3**    
//形式為整數 ， type=int
原本是用來宣告下方的譜面要用什麼方式使用，但現在沒用    

**BPM 280**    
//形式為整數 ， type=int    
歌曲的BPM，用來調整速度    

**PAGE_SHIFT 1.799999**    
//形式為浮點數 ， type=float    
掃線開始的位置，雖然在Cytus2上無法用，但在製作V2譜面就有用了

**PAGE_SIZE 0.857142**    
//形式為浮點數 ， type=float    
掃線每掃一幕(or屏)所需要的時間    

**scan_line_direction_opposite 1**    
//形式為整數 ， type=int ； 只能輸入0或1 (only 0 or 1)    
//預設為0 ， Default 0    
掃線初始方向，一般來說為0，但如果實際方向相反的話可以調為1，他會再反過來。    

**extension_of_time 0**    
//形式為浮點數 ， type=float    
//預設為0 ， Default 0    
整體時間延遲或減少 如果為-3會全譜面的時間-3秒，4的話則全體+4秒    

**auto_fix_type 0**    
//形式為整數 ， type=int ； 只能輸入0或1 (only 0 or 1)    
//預設為0 ， Default 0    
自動幫忙修正HOLD溢出邊界的問題，但不保證效果，預期是如果你的HOLD長度小於該幕的總長且很接近邊界，這時後會自動把該HOLD移到下一幕中，如果是HOLD長度大於該幕的總長則會把note型態變成LONG

**format_version 0**    
//形式為整數 ， type=int ；    
//預設為0 ， Default 0    
這是設定最後輸出譜面時的版本，基本上還是用0就好        

**beat 4**    
//形式為整數 ， type=int ；    
//預設為4 ， Default 4    
歌曲的節拍數，通常都是4拍，極少數情況是3拍    


**time_base 480**    
//形式為整數 ， type=int ；    
//預設為480 ， Default 480    
這個我也不太清楚，但知道設480就對了，估計跟一幕的"質量"有關    

**conversion_constant 60000000**    
//形式為整數 ， type=int ；    
//預設為60000000 ， Default 60000000    
這個是 秒數s 與 tick 換算關係的轉換常數，一般來說不用改，但如果你發現一開始note的時間是準的，到後面越來越不準，則可以細部微調，或者先試試改成 59999940 看看，不行那就自己在微調。    

//================================================    

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
(note型態)-(id)-(出現時間)-(出線時的x座標)-(持續時間)    
(字串string)-(整數int)-(浮點數float)-(浮點數float)-(浮點數float)    

**note型態**：    
有 **NOTE、HOLD、LONG、SLIDE**    
分別是 點、長條、黃色超級長條、切    
然後 HOLD、LONG、SLIDE 是強制型態    

另外完全兼容V2格式，如果你想用出 HOLD 也是可以用    
NOTE	6	11.499799	0.500000	0.754260    
這種方式是可以接受的。    
#### LINK 的格式如下：    
(LINK)-(目標id)-(目標id)-(目標id)....    
(字串string)-(整數int)-(整數int)-(整數int)...    

這個東西會將所選中的 note **強制轉成 LINK 型態**，請務必注意此特性。    
#### CHC 格式如下：    
(CHC)-(變速方式)-(作用時間)    
(字串string)-(整數int)-(浮點數float)

如果要提示掃線速度變快，則可以用CHC達成    
變速方式 輸入  1 等於文字提示 "speed up"，且掃線顏色變 紅(R)    
變速方式 輸入 -1 等於文字提示 "speed down"，且掃線顏色變 綠(G)    
之後可能補上 0 變白色且沒文字    

#### BPM 格式如下：    
(BPM)-(預變的BPM)-(作用時間)    
(字串string)-(整數int)-(浮點數float)    

預變的BPM，如果一開始你的BPM是280，那你在此輸入560就等於兩倍快撥放。    

作用的時間只能是掃線到上下邊界的時間，可容許一點點的誤差，不要超過一幕掃線時間的6分之一為佳。    

此外 BPM作用時間 的部分可以用 TPV4.9 去自動生出來，請善加利用！    
![Imgur](https://i.imgur.com/aO3yNcm.png)
