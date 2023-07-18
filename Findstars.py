from time import sleep
import pymysql
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta

class FindStar: 
    def __init__(self) -> None:
        self.driver = uc.Chrome(browser_executable_path=r"C:\\Users\\v99sa\\Desktop\\chrome-win\\chrome.exe", options=self.__get_ChromeOptions(), version_main=110)
        self.driver.get('https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=3959576&recomd_id=hotSale&cid=recitri&oid=BfG&mdiv=&ctype=B')
        self.wait = WebDriverWait(self.driver, 20)
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

    def findProduct(self):
        # 評論數
        comments = self.driver.find_element(By.XPATH, "//li[@class = 'goodsCommendLi']")
        comments.click()
        # 總星星數
        star = self.driver.find_element(By.XPATH, "//div[@class = 'indicatorAvg']//div[@class = 'indicatorAvgVal']")
        #print(star.get_attribute("outerHTML"))
        #print(comments.get_attribute("outerHTML"))
        print(star.get_attribute("textContent"))
        print(comments.text)

f = FindStar()
f.findProduct() 
