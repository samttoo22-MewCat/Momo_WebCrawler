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
        self.getSubCatagories2("化妝水", "品牌", "string")
    
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
    def getCatagories(self, outType):
        catagories = self.driver.find_element(By.ID, "bt_cate_top")
        if(outType == "webElement"):
            return catagories
        elif(outType == "string"):
            return catagories.text
    
    def goToCatagoryLink(self, catagory):
        wait = WebDriverWait(self.driver, 20)
        
        #要先打開大分類才會出現小分類
        catagoryBotton = self.getCatagories("webElement")
        catagoryBotton = catagoryBotton.find_element(By.XPATH, ".//a[contains(text(),'%s')]" % catagory)
        catagoryLink = catagoryBotton.get_attribute("href")
        
        #轉到大分類的的連結
        self.driver.get(catagoryLink)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//th[contains(text(),'品牌')]")))
    #找出小分類    
    def getSubCatagories1(self, catagory, outType):
        self.goToCatagoryLink()
                
        rawLists = self.driver.find_elements(By.XPATH, "//table[@class = 'wrapTable']//tbody//tr")
        if(outType == "webElement"):
            return rawLists
        elif(outType == "string"):
            subCatagories = []
            for r in rawLists:
                subCatagories.append(r.get_attribute("indexname"))
                
                
    #找出小分類中的 小小分類列表
    def getSubCatagories2(self, catagory, subCatagory1, outType):
        self.goToCatagoryLink(catagory)
        
        subCatagories2 = self.driver.find_elements(By.XPATH, "//table[@class = 'wrapTable']//tbody//tr")
            
        for s in subCatagories2:
            subCatagories1Name = s.get_attribute("indexname")
            if(subCatagories1Name == subCatagory1):
                subCatagories2 = s.find_elements(By.XPATH, ".//td//div[@class = 'wrapDiv']//ul//li//label")
                break
            
        #分成輸出元素還是純文字
        if(outType == "webElement"):
            return subCatagories2
        elif(outType == "string"):
            subCatagories2List = []
            for b in subCatagories2:
                subCatagories2List.append(b.get_attribute("title"))
            return subCatagories2List
    
    def getFitsOnTypes(self, catagory):
        pass
c = Category()