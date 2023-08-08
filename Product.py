import requests
from selenium import webdriver
# -*- coding: UTF-8 -*-
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from datetime import datetime, timedelta
import json
import gc
import pymysql

class Product(object):
    def __init__(self,executable_path, url, userAgent) -> None:
        self._executable_path = executable_path
        self._url = url
        self._useragent = userAgent

        self.driver = uc.Chrome( browser_executable_path = self._executable_path , options=self.__get_ChromeOptions())
        self.driver.get( self._url )
        self.wait = WebDriverWait(self.driver, 20)
        self.headers = {
            'User-Agent': self._useragent
        }

        pageSource = self.driver.page_source.encode("utf-8")
        self.soup = BeautifulSoup(pageSource,'lxml')

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
            return options
    def returnURL(self):
        return self._url
    def getProductInfo(self):
        # 商品名稱
        name = str(self.soup.find(id = 'osmGoodsName').text)
        # 最折扣價格
        price = self.soup.find("meta", property="product:price:amount")
        # 品牌名稱
        brand = self.soup.find("meta", property="product:brand")
        # 品號
        productid = self.soup.find("meta", property="product:retailer_item_id")
        
        # 商品規格表格讀取
        table = self.soup.find('div', {'class': 'attributesArea'}).find('table')
        columns =  [tr for tr in table.findAll('tr')]
        tds = [ column.find("td") for column in columns ]
        # 商品規格 - 品牌系列名稱
        series = tds[1].text
        # 商品規格 - 專櫃
        brandtype =  tds[2].text
        # 商品規格 - 包裝組合
        package =  str(tds[3]).replace('<td>',"").replace('<ul>',"").replace('<li>',"").replace('</li>',"*").replace('</ul>',"").replace('</td>',"")
        # 商品規格 - 功效
        function = str(tds[4]).replace('<td>',"").replace('<ul>',"").replace('<li>',"").replace('</li>',"*").replace('</ul>',"").replace('</td>',"")
        # 商品規格 - 適用於
        usage = str(tds[5]).replace('<td>',"").replace('<ul>',"").replace('<li>',"").replace('</li>',"*").replace('</ul>',"").replace('</td>',"")
       
        # 銷售量
        sales =  self.driver.find_element(By.XPATH, "//div[@class = 'productRatingFlex']//p[@class = 'productTotalSales']") 
        # 評論數
        comments = self.driver.find_element(By.XPATH, "//li[@class = 'goodsCommendLi']")
        if comments.text == "商品評價(0)" :
             starCount = 0 
        else:
            comments.click()
        # 總星星數
        star = self.driver.find_element(By.XPATH, "//div[@class = 'indicatorAvg']//div[@class = 'indicatorAvgVal']")
        starCount = star.get_attribute("textContent")
        comments = str(comments.text).replace('商品評價(','').replace(')','')

        
        ProductJson = {
            "name": name,
            "id": productid["content"], 
            "price":price["content"],
            "brand": brand["content"],
            "brandtype": brandtype,
            "series":series,
            "package":package, 
            "function":function, 
            "usage":usage, 
            "sales":sales.text,
            "comments":comments, 
            "star":starCount
        }
        return ProductJson
    
p = Product("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",'https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=9007774&recomd_id=hotSale&cid=recitri&oid=BfG&mdiv=&ctype=B', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
json_object = p.getProductInfo() 
json_formatted_str = json.dumps(json_object, ensure_ascii = False, indent=2)
print(json_formatted_str)

