# -*- coding: UTF-8 -*-
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import undetected_chromedriver as uc

class Product(object):
    def __init__(self, driver, useragent) -> None:
        self.driver = driver
        self._useragent = useragent
        
        
        self.wait = WebDriverWait(self.driver, 20)
        self.headers = {
            'User-Agent': self._useragent
        }

        

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
    def getProductInfo(self, url):
        self.driver.get(url)
        pageSource = self.driver.page_source.encode("utf-8")
        soup = BeautifulSoup(pageSource,'lxml')
        # 商品名稱
        name = str(soup.find(id = 'osmGoodsName').text)
        # 最終折扣價格
        price = soup.find("meta", property="product:price:amount")
        # 品牌名稱
        brand = soup.find("meta", property="product:brand")
        # 品號
        productid = soup.find("meta", property="product:retailer_item_id")
        
        # 商品規格表格讀取
        table = soup.find('div', {'class': 'attributesArea'}).find('table')
        columns =  [tr for tr in table.findAll('tr')]
        tds = [ column.find("td") for column in columns ]
        ths = []
            # 防止出現折扣後 Error 
        for column in columns:
            try:
                ths.append(column.find("th").text)
            except:
                
                print(url)
                print(column)
        
        # 商品規格 - 品牌系列名稱
        seriesNum = ths.index("品牌系列名稱") if "品牌系列名稱" in ths else -1
        if seriesNum == -1 :
            series = None
        else:
            series = tds[seriesNum].text
        # 商品規格 - 品牌定位
        brandtypeNum = ths.index("品牌定位") if "品牌定位" in ths else -1
        if  brandtypeNum == -1 :
            brandtype = None
        else:
           brandtype = tds[brandtypeNum].text
        # 商品規格 - 包裝組合
        packageNum = ths.index("包裝組合") if "包裝組合" in ths else -1
        if  packageNum == -1 :
            package = None
        else:
            package =  str(tds[packageNum]).replace('<td>',"").replace('<ul>',"").replace('<li>',"").replace('</li>',"*").replace('</ul>',"").replace('</td>',"")
        # 商品規格 - 功效
        functionNum = ths.index("功效") if "功效" in ths else -1
        if  functionNum == -1 :
            function= None
        else:
            function = str(tds[functionNum]).replace('<td>',"").replace('<ul>',"").replace('<li>',"").replace('</li>',"*").replace('</ul>',"").replace('</td>',"")
        # 商品規格 - 適用於
        usageNum = ths.index("適用於") if "適用於" in ths else -1
        if  usageNum == -1 :
            usage = None
        else:
            usage = str(tds[usageNum]).replace('<td>',"").replace('<ul>',"").replace('<li>',"").replace('</li>',"*").replace('</ul>',"").replace('</td>',"")
        # 銷售量
        #self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='productRatingFlex']/p")))
        try:
            sales =  self.driver.find_element(By.XPATH, "//*[@id='productRatingFlex']/p") 
            sales = sales.get_attribute("textContent")
        except:
            sales = "0"
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

        ProductDict = {
            "name": name,
            "id": productid["content"], 
            "price":price["content"],
            "brand": brand["content"],
            "brandtype": brandtype,
            "series":series,
            "package":package, 
            "function":function, 
            "usage":usage, 
            "sales":sales,
            "comments":comments, 
            "star":starCount
        }
        return ProductDict

