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
    def __init__(self, driver) -> None:
        self.driver = driver
        self.driver.get('https://www.momoshop.com.tw/category/LgrpCategory.jsp?l_code=1111700000&sourcePageType=4')
        self.wait = WebDriverWait(self.driver, 20)
    
    #找出大分類    
    def getCategories(self, outType):
        categories = self.driver.find_element(By.ID, "bt_cate_top")
        if(outType == "webElement"):
            return categories
        elif(outType == "string"):
            return categories.text.split(" ")
    
    def goToCategoryLink(self, category):
        #要先打開大分類才會出現小分類
        categoryBotton = self.getCategories("webElement")
        categoryBotton = categoryBotton.find_element(By.XPATH, ".//a[contains(text(),'%s')]" % category)
        categoryLink = categoryBotton.get_attribute("href")
        
        #轉到大分類的的連結
        self.driver.get(categoryLink)
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//th[contains(text(),'品牌')]")))
    #找出小分類    
    def getSubCategories1(self, category, outType):
        try:
            self.goToCategoryLink(category)
        except:
            print("無此大分類")        
        rawLists = self.driver.find_elements(By.XPATH, "//table[@class = 'wrapTable']//tbody//tr")
        if(outType == "webElement"):
            return rawLists
        elif(outType == "string"):
            subCategories = []
            for r in rawLists:
                #print(r.get_attribute("indexname"))
                subCategories.append(r.get_attribute("indexname"))
            return subCategories
                
                
    #找出小分類中的 小小分類列表
    def getSubCategories2(self, subCategory1, outType):
        subCategories2 = self.driver.find_elements(By.XPATH, "//table[@class = 'wrapTable']//tbody//tr")
            
        for s in subCategories2:
            subCategories1Name = s.get_attribute("indexname")
            if(subCategories1Name == subCategory1):
                subCategories2 = s.find_elements(By.XPATH, ".//td//div[@class = 'wrapDiv']//ul//li//label")
                break
            
        #分成輸出元素還是純文字
        if(outType == "webElement"):
            return subCategories2
        elif(outType == "string"):
            subCategories2List = []
            for b in subCategories2:
                if(b.get_attribute("title") == None):
                    pass
                #print(b.get_attribute("outerHTML"))
                subCategories2List.append(b.get_attribute("title"))
            return subCategories2List
    
    
    def selectSubCate2(self, subCate1, subCate2):
        subCates2 = self.getSubCategories2(subCate1, "webElement")
        '''
        openCate2List = self.driver.find_elements(By.XPATH, "//table[@class = 'wrapTable']//tbody//tr")
        for o in openCate2List:
            if(o.get_attribute("indexname") == subCate1):
                openCate2List = o.find_element(By.XPATH, ".//td//a[@class = 'multipleChoiceBtn']")
                break
        
        self.wait.until(EC.element_to_be_clickable(openCate2List))
        openCate2List.click()
        '''
        for s in subCates2:
            if(subCate2 in s.get_attribute("title")):
                print("yes")
                #self.wait.until(EC.element_to_be_clickable(s))
                self.driver.execute_script("(arguments[0]).click();", s)
                #s.click()
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
                
