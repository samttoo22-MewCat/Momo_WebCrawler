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
        
    def getCatagories(self, type):
        catagories = self.driver.find_element(By.ID, "bt_cate_top")
        if(type == "webElement"):
            return catagories
        elif(type == "string"):
            return catagories.text
        
    def getRawLists(self):
        wait = WebDriverWait(self.driver, 20)
        
        catagoryBotton = self.getCatagories()
        catagoryBotton = catagoryBotton.find_element(By.XPATH, ".//a[contains(text(),'%s')]" % "化妝水")
        catagoryLink = catagoryBotton.get_attribute("href")
        print(catagoryLink)
        #self.driver.execute_script("window.open('%s');" % catagoryLink)
        #self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(catagoryLink)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//th[contains(text(),'品牌')]")))
                
        rawLists = self.driver.find_elements(By.XPATH, "//table[@class = 'wrapTable']//tbody")
        return rawLists
    def getBrandList(self, catagory, type):
        wait = WebDriverWait(self.driver, 20)
        
        catagoryBotton = self.getCatagories("webElement")
        catagoryBotton = catagoryBotton.find_element(By.XPATH, ".//a[contains(text(),'%s')]" % catagory)
        catagoryLink = catagoryBotton.get_attribute("href")
        print(catagoryLink)
        #self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(catagoryLink)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//th[contains(text(),'品牌')]")))
                
        brandList = self.driver.find_element(By.XPATH, "//table[@class = 'wrapTable']//tbody")
        print(brandList.get_attribute("outerHTML"))
        if(type == "webElement"):
            return brandList
        elif(type == "string"):
            return brandList.text
    
c = Category()