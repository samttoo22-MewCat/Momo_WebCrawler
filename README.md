## Momo_WebCrawler 
這個程式是一個用來爬取 Momo 網站上商品資訊的網路爬蟲工具。它可以讓使用者選擇不同的商品類別、大分類和小分類，然後爬取相關商品的資訊並輸出為 JSON 格式的檔案。


## 開發進度

<input type="checkbox" checked> 臉部保養爬蟲模組<br>
&ensp;|_ [臉部保養](https://www.momoshop.com.tw/category/LgrpCategory.jsp?l_code=1111700000&sourcePageType=4)<br>
&ensp;&ensp;|_ <font color=#e40580>( 類別 )</font> 化妝水, 精華液, 乳液, 乳霜, 凝膠, 面膜, 眼霜, 護唇膏, 防曬, 素顏霜, 美頸霜, 保養超值組<br>
&ensp;&ensp;&ensp;|_ <font color=#e40580>( 大分類 )</font>  品牌, 適用於, 功效, 包裝組合, 品牌定位 ... <br>
&ensp;&ensp;&ensp;&ensp; |_ <font color=#e40580>( 小分類 )</font>  單入組, 乾肌, 敏感肌, 專櫃品牌 ... <br>
&ensp;&ensp;&ensp;&ensp;&ensp; |_  <font color=#e40580>( 各商品 )</font>  商品名稱,  最終折扣價格, 品牌名稱, 品號, 商品規格-品牌系列名稱,  商品規格-品牌定位, 商品規格-包裝組合, 商品規格-功效, 商品規格-適用於, 銷售量, 評論數, 總星星數<br>
&ensp;&ensp;&ensp;&ensp;&ensp; -> 輸出為 json 檔

<input type="checkbox" > 化妝品爬蟲模組<br>

## 下載


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

- 電子郵件：你的郵件地址
- 社群平台：你的社群帳號

感謝你使用本程式，希望能對你的研究和學習有所幫助！
