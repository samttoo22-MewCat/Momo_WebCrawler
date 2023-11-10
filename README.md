## Momo_WebCrawler 
這個程式是一個用來爬取 Momo 網站上商品資訊的網路爬蟲工具。它可以讓使用者選擇Momo購物網站的特定分類，然後爬取相關商品的資訊並輸出為 JSON 格式的檔案。 <br>
此程式是 kiwiiiiiiiiO 和 samttoo22-MewCat 所開發。 <br>


## 開發進度

- [x] 全網站抓取資料之功能<br>
&ensp;|_ $\color{#e40580}{( Cate0 )}$ 3C, 家電, 美妝個清, 保健/食品, 服飾/內衣, 鞋包/精品, 母嬰用品, 圖書文具, 傢寢運動, 日用生活, 旅遊戶外 <br>
&ensp;&ensp;|_  $\color{#e40580}{( Cate1 )}$ <br>
&ensp;&ensp;&ensp;|_ $\color{#e40580}{( Cate2 )}$ <br>
&ensp;&ensp;&ensp;&ensp; |_ $\color{#e40580}{( Cate3 )}$ <br>
&ensp;&ensp;&ensp;&ensp;&ensp; |_  $\color{#e40580}{( Cate4 )}$ <br>
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp; |_  $\color{#e40580}{( Cate5 )}$ <br>
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp; -> 輸出為 json 檔 <br>
Cate 0 - 5分類分別是指哪個請看下面圖片。 <br>
Cate 0 後的分類因為不固定，故不在此列出。 <br>
![image](https://github.com/samttoo22-MewCat/Momo_WebCrawler/blob/main/tutorial1.png) <br>
![image](https://github.com/samttoo22-MewCat/Momo_WebCrawler/blob/main/tutorial2.png) <br>

- [ ] 使用者介面與教學<br>
- [x] 多執行緒<br>
使用異部函數讓效率變好了，之前只能一次抓一個，現在可以同時抓十幾個Cate3，總之大概快個五到十倍吧。<br>
代價就是電腦會開始燃燒(?)<br>
## 下載
之後預計會包裝成EXE檔，裡面包含使用者介面與教學
## 環境設定
在使用之前，請確保已經安裝了以下必要的軟體和套件：

- Python 3.x
- 爬蟲套件
  1. undetected_chromedriver 
  這是一個能夠避免被偵測到的 ChromeDriver。<br>
      ```pip install undetected-chromedriver```
  
  2. selenium<br>
  ```pip install selenium```

  3. bs4<br>
   ```pip install  bs4```


## 適用瀏覽器

|  Google Chrome  |
|  ----  |
|  目前 chromedriver 最高支援到 114 版本之瀏覽器<br/>，如果已經更新，可以選擇降級至較低版本  |


## 開始使用
1. 下載這個程式的程式碼並保存到你的電腦上。

2. 開啟 Main.py 檔案，這是程式的主要執行檔案。

3. 編輯 Main.py 中的以下設定，以便與你的系統環境相符：
  - 設定 Chrome 瀏覽器的執行路徑：將 browser_executable_path 變數設定為你的 Chrome 執行檔案路徑。
  - 設定使用者資料目錄：將 user-data-dir 參數設定為你的 Chrome 使用者資料目錄。

4. 在終端機中切換到程式碼所在的目錄，執行以下指令來運行程式：
  <br>```python Main.py```

5. 程式將會提示你選擇商品的類別、大分類和小分類。根據提示進行選擇，直到所有分類都被選取完畢。

6. 程式將開始爬取所選取分類下的商品資訊，並將結果輸出為 JSON 格式的檔案。

7. 輸出的 JSON 檔案將包含所選取分類的商品資訊，包括商品名稱、價格、評分...等。

* 教學影片


## 注意事項
- 本程式僅供學習和研究使用，請勿用於商業用途或違法行為。
- 爬取網站資訊時請遵循網站的使用條款與政策，以避免觸犯法律或造成損害。
- 運行程式時可能會遇到反爬機制，請謹慎使用程式以避免被偵測或封鎖。


## 聯絡方式
如果你有任何問題或建議，歡迎通過以下方式聯絡我們：

- 電子郵件：
    - samttoo22-MewCat：v99sam@gmail.com

感謝你使用本程式，希望能對你的研究和學習有所幫助！
