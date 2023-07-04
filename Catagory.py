from time import sleep
import pymysql
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta

class Category():
    def __init__(self) -> None:
        self.driver = uc.Chrome(browser_executable_path=r"C:\\Users\\v99sa\\Desktop\\chrome-win\\chrome.exe", options=self.__get_ChromeOptions(), version_main=110)
        self.driver.get('https://www.momoshop.com.tw/category/LgrpCategory.jsp?l_code=1111700000&sourcePageType=4')
        self.getBrandList("化妝水")
    
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
        
    def getCatagories(self):
        catagories = self.driver.find_element(By.ID, "bt_cate_top")
        return catagories
        
    def getBrandList(self, catagory):
        wait = WebDriverWait(self.driver, 20)
        
        catagoryBotton = self.getCatagories()
        catagoryBotton = catagoryBotton.find_elements(By.XPATH, ".//a")
        for c in catagoryBotton:
            print(c.text)
            print(c.get_attribute("href"))
                
        #brandList = self.driver.find_element(By.ID, "brandsList")
        #print(brandList.text)
        #return brandList
    
c = Category()