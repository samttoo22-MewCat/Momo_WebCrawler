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
    
    #找出大分類    
    def getCatagories(self, outType):
        catagories = self.driver.find_element(By.ID, "bt_cate_top")
        if(outType == "webElement"):
            return catagories
        elif(outType == "string"):
            return catagories.text
    
    def goToCatagoryLink(self, catagory):
        #要先打開大分類才會出現小分類
        catagoryBotton = self.getCatagories("webElement")
        catagoryBotton = catagoryBotton.find_element(By.XPATH, ".//a[contains(text(),'%s')]" % catagory)
        catagoryLink = catagoryBotton.get_attribute("href")
        
        #轉到大分類的的連結
        self.driver.get(catagoryLink)
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//th[contains(text(),'品牌')]")))
    #找出小分類    
    def getSubCatagories1(self, catagory, outType):
        try:
            self.goToCatagoryLink(catagory)
        except:
            print("無此大分類")        
        rawLists = self.driver.find_elements(By.XPATH, "//table[@class = 'wrapTable']//tbody//tr")
        if(outType == "webElement"):
            return rawLists
        elif(outType == "string"):
            subCatagories = []
            for r in rawLists:
                #print(r.get_attribute("indexname"))
                subCatagories.append(r.get_attribute("indexname"))
                
                
    #找出小分類中的 小小分類列表
    def getSubCatagories2(self, subCatagory1, outType):
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
                if(b.get_attribute("title") == None):
                    pass
                print(b.get_attribute("title"))
                #print(b.get_attribute("outerHTML"))
                subCatagories2List.append(b.get_attribute("title"))
            return subCatagories2List
    
    
    def selectSubCata2(self, subCata1, subCata2):
        subCatas2 = self.getSubCatagories2(subCata1, "webElement")
        for s in subCatas2:
            if(subCata2 in s.get_attribute("title")):
                self.wait.until(EC.element_to_be_clickable(s))
                s.click()
                self.wait.until(EC.visibility_of_element_located((By.XPATH, "//label[@class = 'selected']")))
                break
    
    def getProductsLinksList(self):
        def getPages():
            pages = self.driver.find_element(By.XPATH, "//li[contains(text(),'頁數')]")
            return pages.text.split(" ")[-1]
        def getPageNow():
            pages = self.driver.find_element(By.XPATH, "//li[contains(text(),'頁數')]")
            return pages.text.split(" ")[-3]
        def goToNextPage():
            nextPageBotton = self.driver.find_element(By.XPATH, "//a[contains(text(),'下一頁')]")
            self.wait.until(EC.element_to_be_clickable(nextPageBotton))
            nextPageBotton.click()
            #self.wait.until(EC.visibility_of_element_located((By.XPATH, "//li[contains(text(),'頁數')]")))
        
        LinksList = []
        pages = int(getPages())
        for page in range(pages):
            products = self.driver.find_elements(By.XPATH, "//div[@class = 'prdListArea bt770class']//ul//li")
            for product in products:
                url = product.find_element(By.XPATH, ".//a[@class = 'prdUrl']").get_attribute("href")
                totalSale = product.find_element(By.XPATH, ".//span[@class = 'totalSales goodsTotalSales']").text.split(">")[-1]
                out = []
                out.append(url)
                out.append(totalSale)
                LinksList.append(out)
            if(page != pages - 1):
                goToNextPage()
        return LinksList
                
c = Category()
c.goToCatagoryLink("化妝水")
#c.getSubCatagories2("品牌", "string")
c.selectSubCata2("功效", "抗痘")
print(c.getProductsLinksList())