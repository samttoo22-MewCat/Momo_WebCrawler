from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import json
import gc
import requests

class Product():
    def __init__(self) -> None:
        self.driver = uc.Chrome(browser_executable_path=r"C:\\Users\\v99sa\\Desktop\\chrome-win\\chrome.exe", options=self.__get_ChromeOptions(), version_main=110)
        self.driver.get('https://www.momoshop.com.tw/category/LgrpCategory.jsp?l_code=1111700000&sourcePageType=4')
        
        self.url = 'https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=9007774&recomd_id=hotSale&cid=recitri&oid=BfG&mdiv=&ctype=B'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        self.res = requests.post(self.url, headers=self.headers)
        self.res.encoding = 'uth-8'
        self.soup = BeautifulSoup(self.res.text,"lxml")
    
    def __get_ChromeOptions(self): 
            options = uc.ChromeOptions()
            options.add_argument('--start_maximized')
            options.add_argument("--disable-extensions")
            options.add_argument('--disable-application-cache')
            options.add_argument('--disable-gpu')
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-notifications")
            options.add_argument("--incognito")
            
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--user-data-dir=C:\\Users\\v99sa\\Desktop\\coding\\py\\Momo_WebCrawler\\Momo_WebCrawler\\profile1")
            return options

    def getProductInfo(self):
        # 商品名稱
        name = self.soup.find(id = 'osmGoodsName').text
        print(name)
        # 最折扣價格
        price = self.soup.find("meta", property="product:price:amount")
        print(price["content"] if price else "No meta price given")
        # 品牌名稱
        brand = self.soup.find("meta", property="product:brand")
        print(brand["content"] if brand else "No meta brnad given")
        # 品號
        productid = self.soup.find("meta", property="product:retailer_item_id")
        print(productid["content"] if productid else "No meta product_id given")

        # 銷售量
        # attributeArea = soup.find('div', {'class': 'productRatingFlex'})
        # print(attributeArea)
        # 評價數
        # 評價星號

        table = self.soup.find('div', {'class': 'attributesArea'}).find('table')
        columns =  [tr for tr in table.findAll('tr')]
        tds = [ column.find("td") for column in columns ]
        # 商品規格 - 品牌定位
        brandtype = tds[1].text
        print(brandtype)
        # 商品規格 - 包裝組合
        package =  tds[2].text
        print(package)
        # 商品規格 - 功效
        function =  str(tds[3]).replace('<td>',"").replace('<ul>',"").replace('<li>',"").replace('</li>',"*").replace('</ul>',"").replace('</td>',"")
        print(function)
        # 商品規格 - 適用於
        usage =  tds[4].text
        print(usage)
