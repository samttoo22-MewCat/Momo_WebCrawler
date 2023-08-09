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
    def __init__(self, driver) -> None:
        self.driver = driver
        
        self.wait = WebDriverWait(self.driver, 20)

    def findProduct(self):
        self.driver.get('https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=3959576&recomd_id=hotSale&cid=recitri&oid=BfG&mdiv=&ctype=B')
        # 評論數
        comments = self.driver.find_element(By.XPATH, "//li[@class = 'goodsCommendLi']")
        comments.click()
        # 總星星數
        star = self.driver.find_element(By.XPATH, "//div[@class = 'indicatorAvg']//div[@class = 'indicatorAvgVal']")
        #print(star.get_attribute("outerHTML"))
        #print(comments.get_attribute("outerHTML"))
        print(star.get_attribute("textContent"))
        print(comments.text)
