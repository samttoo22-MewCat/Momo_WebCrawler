from time import sleep
import pymysql
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta

#類別Cate現在被分為0 - 5
class Category():
    def __init__(self, driver) -> None:
        
        #由外部匯入driver
        self.driver = driver
        #讓driver打開初始網址
        self.driver.get('https://www.momoshop.com.tw/category/LgrpCategory.jsp?l_code=1111700000&sourcePageType=4')
        self.wait = WebDriverWait(self.driver, 20)
    
    def getCate0List(self, outType):
        Cate0 = self.driver.find_element(By.ID, "toothUl")
        if(outType == "webElement"):
            return Cate0
        elif(outType == "string"):
            return Cate0.text.split(" ")
        
    def getCate1List(self, Cate0, outType):
        Cate0Dict = {"3C" : 0, "家電": 1, "美妝個清": 2,
                    "保健/食品": 3, "服飾/內衣": 4, "鞋包/精品": 5,
                    "母嬰用品": 6, "圖書文具": 7, "傢寢運動": 8,
                    "日用生活": 9, "旅遊戶外": 10}
        CateIndex = Cate0Dict[Cate0]
        rawCate1 = self.driver.find_elements(By.XPATH, "//*[@id='bt_0_layout_b1096']//div[@class='btclass navcontent_innerwarp category2019']")
        Cate1 = rawCate1[CateIndex]
        Cate1 = Cate1.find_elements(By.XPATH, ".//div[@class='contenttop topArea']//table//tbody//tr//td//p") 
                
        if(outType == "webElement"):
            return Cate1
        elif(outType == "string"):
            out = []
            for c in Cate1:
                out.append(c.get_attribute("textContent"))
            return out
    
    #從Cate0 和 Cate1 找出 Cate2 列表    
    def getCate2List(self, Cate0, Cate1, outType):
        CateDict = {"3C": 0, "家電": 1, "美妝個清": 2,
                    "保健/食品": 3, "服飾/內衣": 4, "鞋包/精品": 5,
                    "母嬰用品": 6, "圖書文具": 7, "傢寢運動": 8,
                    "日用生活": 9, "旅遊戶外": 10}
        i = 0
        #把Cate1轉換成字典
        Cate1Dict = {}
        for c in self.getCate1List(Cate0, "string"):
            Cate1Dict[c] = i
            i += 1
            
        CateIndex = CateDict[Cate0]
        Cate1Index = Cate1Dict[Cate1]
        rawCate1 = self.driver.find_elements(By.XPATH, "//*[@id='bt_0_layout_b1096']//div[@class='btclass navcontent_innerwarp category2019']")
        Cate1 = rawCate1[CateIndex]
        Cate1 = Cate1.find_elements(By.XPATH, ".//div[@class='contenttop topArea']//table//tbody//tr//td") 
        Cate2 = Cate1[Cate1Index]
        Cate2 = Cate2.find_elements(By.XPATH, ".//ul//li//a") 
        
        
        if(outType == "webElement"):
            return Cate2
        elif(outType == "string"):
            out = []
            for c in Cate2:
                out.append(c.get_attribute("textContent"))
            return out
    
    #從Cate0, Cate1, 和選定的Cate2 中前往 Cate2 的連結  
    def goToCate2List(self, Cate0, Cate1, Cate2):
        Cate2 = self.getCate2List(Cate0, Cate1, "webElement")
        for c in Cate2:
            Cate2Name = c.get_attribute("textContent")
            if(Cate2Name == Cate2):
                self.driver.get(c.get_attribute("href"))
                break
        
    #找出Cate3
    def getCate3List(self, outType):
        #找出id為"bt_cate_top"的網頁元素，即為類別列表的網頁元素
        Cate3 = self.driver.find_element(By.ID, "bt_cate_top")
        #用網頁元素回傳還是回傳字串
        if(outType == "webElement"):
            return Cate3
        elif(outType == "string"):
            return Cate3.text.split(" ")
    
    #打開Cate3
    def goToCate3Link(self, Cate3):
        #要先打開大分類才會出現小分類
        #拿到類別列表的網頁元素
        Cate3Botton = self.getCate3List("webElement")
        #從類別底下再找到特定類別
        Cate3Botton = Cate3Botton.find_element(By.XPATH, ".//a[contains(text(),'%s')]" % Cate3)
        #拿到該特定類別的連結
        Cate3Link = Cate3Botton.get_attribute("href")
        
        #進入該特定類別的連結
        self.driver.get(Cate3Link)
        #進入後要等到大類別出現
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//th[contains(text(),'品牌')]")))
    
    #從Cate3中找出Cate4 列表
    def getCate4List(self, Cate3, outType):
        #試著進入此類別連結，無法則代表此類別存不存在
        try:
            self.goToCate3Link(Cate3)
        except:
            print("無此類別")  
        
        #成功進入此類別連結後，從以下的路徑找出大類別類表
        rawLists = self.driver.find_elements(By.XPATH, "//table[@class = 'wrapTable']//tbody//tr")
        
        #輸出網頁元素還是字串
        if(outType == "webElement"):
            return rawLists
        elif(outType == "string"):
            out = []
            for r in rawLists:
                out.append(r.get_attribute("indexname"))
            out.pop()
            return out
                         
    #從Cate4中找出Cate5 列表
    def getCate5List(self, Cate4, outType):
        #從以下路徑找出小分類列表
        Cate5 = self.driver.find_elements(By.XPATH, "//table[@class = 'wrapTable']//tbody//tr")
        for s in Cate5:
            Cate4Name = s.get_attribute("indexname")
            if(Cate4Name == Cate4):
                Cate5 = s.find_elements(By.XPATH, ".//td//div[@class = 'wrapDiv']//ul//li//label")
                break
            
        #輸出網頁元素還是文字
        if(outType == "webElement"):
            return Cate5
        elif(outType == "string"):
            Cate5List = []
            for b in Cate5:
                if(b.get_attribute("title") == None):
                    pass
                #print(b.get_attribute("outerHTML"))
                Cate5List.append(b.get_attribute("title"))
            return Cate5List
    
    #從 Cate4 選擇指定的 Cate5
    def selectCate5(self, Cate4, Cate5):
        Cate5Name = Cate5
        #拿到小分類列表的網頁元素
        Cate5List = self.getCate5List(Cate4, "webElement")
        
        #從小分類列表裡面找出要選的小分類，然後點擊他
        for s in Cate5List:
            if(Cate5Name in s.get_attribute("title")):
                print("已選取" + Cate5)
                #小分類可能是隱藏看不到的，所以要用js的方式下指令點擊
                self.driver.execute_script("(arguments[0]).click();", s)
                self.wait.until(EC.visibility_of_element_located((By.XPATH, "//label[@class = 'selected']")))
                break
    
    #獲取最終選完小分類的所有商品連結
    def getProductsLinksList(self):
        #抓總頁數
        def getPages():
            try:
                pages = self.driver.find_element(By.XPATH, "//li[contains(text(),'頁數')]")
                return pages.text.split(" ")[-1]
            except:
                return 0

        #前往下一頁
        def goToNextPage():
            nextPageBotton = self.driver.find_element(By.XPATH, "//div[@class = 'pageArea']//dl//dd//a[contains(text(),'下一頁')]")
            self.wait.until(EC.element_to_be_clickable(nextPageBotton))
            nextPageBotton.click()
            self.wait.until(EC.visibility_of_all_elements_located)
        
        LinksList = []
        pages = int(getPages())
        print("總共" + str(pages) + "頁，開始蒐集連結...\n(網站的頁面不一定正確，對我試過了，反正超過或少於都很正常)\n")
        
        #跑過每一頁
        page = 1
        while(True):
            #抓出當頁所有商品
            products = self.driver.find_elements(By.XPATH, "//div[@class = 'prdListArea bt770class']//ul//li")
            #遍歷商品
            for product in products:
                url = product.find_element(By.XPATH, ".//a[@class = 'prdUrl']").get_attribute("href")
                totalSale = product.find_element(By.XPATH, ".//span[@class = 'totalSales goodsTotalSales']").text.split(">")[-1]
                out = []
                out.append(url)
                out.append(totalSale)
                LinksList.append(out)          
            try:
                #如果還沒到最後一頁
                if(EC.invisibility_of_element((By.XPATH, "//div[@class = 'adjustmentTextArea']"))):
                    goToNextPage()
                    print("第 " + str(page) + " 頁完成。")
                #到最後一頁了
                else:
                    break
            #到最後一頁了
            except:
                break
            page += 1
        print("商品連結收集完成。\n")
        print("總共" + str(len(LinksList)) + "個商品。\n")
        
        return LinksList



