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
        self.getBrandList("化妝水", "string")
    
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
    
    #找出大分類    
    def getCatagories(self, type):
        catagories = self.driver.find_element(By.ID, "bt_cate_top")
        if(type == "webElement"):
            return catagories
        elif(type == "string"):
            return catagories.text
    
    #找出小分類    
    def getRawLists(self):
        wait = WebDriverWait(self.driver, 20)
        
        catagoryBotton = self.getCatagories()
        catagoryBotton = catagoryBotton.find_element(By.XPATH, ".//a[contains(text(),'%s')]" % "化妝水")
        catagoryLink = catagoryBotton.get_attribute("href")
        print(catagoryLink)
        
        self.driver.get(catagoryLink)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//th[contains(text(),'品牌')]")))
                
        rawLists = self.driver.find_elements(By.XPATH, "//table[@class = 'wrapTable']//tbody")
        return rawLists
    
    #找出小分類中的 "品牌"
    def getBrandList(self, catagory, type):
        wait = WebDriverWait(self.driver, 20)
        
        #拿到類別的按鈕和連結
        catagoryBotton = self.getCatagories("webElement")
        catagoryBotton = catagoryBotton.find_element(By.XPATH, ".//a[contains(text(),'%s')]" % catagory)
        catagoryLink = catagoryBotton.get_attribute("href")
        
        #轉到類別的連結，然後等待到類別下小分類顯示出來
        self.driver.get(catagoryLink)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//th[contains(text(),'品牌')]")))
        
        #小分類的按鈕列表
        brandListBottons = self.driver.find_elements(By.XPATH, "//table[@class = 'wrapTable']//tbody//tr//td//div[@class= 'wrapDiv']//ul[@id = 'brandsList']//li//label")
        
        #分成輸出元素還是純文字
        if(type == "webElement"):
            return brandListBottons
        elif(type == "string"):
            brandList = []
            for b in brandListBottons:
                brandList.append(b.get_attribute("title"))
            return brandList
    
c = Category()