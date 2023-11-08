import json
import os

import Category, Product
import undetected_chromedriver as uc
from datetime import datetime


class Main():
    def __init__(self) -> None:
        #瀏覽器設定
        def __get_ChromeOptions(): 
            options = uc.ChromeOptions()
            options.add_argument('--start_maximized')
            options.add_argument("--disable-extensions")
            options.add_argument('--disable-application-cache')
            options.add_argument('--disable-gpu')
            options.add_argument('--headless') 
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-notifications")
            options.add_argument("--incognito")
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
            options.add_argument(f'user-agent={user_agent}')
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--user-data-dir=C:\\Users\\v99sa\\Desktop\\coding\\py\\Momo_WebCrawler\\Momo_WebCrawler\\profile1")
            return options
        self.driver = uc.Chrome(browser_executable_path=r"C:\\Users\\v99sa\\Desktop\\chrome-win\\chrome.exe", options=__get_ChromeOptions(), version_main=110)
        self.category = Category.Category(self.driver)
        self.product = Product.Product(self.driver, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
        
        #儲存類別0~5
        self.theCate0 = ""
        self.theCate1 = ""
        self.theCate2 = ""
        self.theCate3 = ""
        self.theCate4 = ""
        self.theCate5 = []
        
        #print(self.category.getCate1List("美妝個清", "string"))
        #print(self.category.getCate2List("美妝個清", "臉部保養", "string"))
        #self.category.goToCate2("美妝個清", "臉部保養", "化妝水")
        #print(self.category.getCate3List("string"))
        #self.category.goToCate3Link("精華液")
        #print(self.category.getCate4List("精華液", "string"))
        #print(self.category.getCate5List("品牌", "string"))
        #self.category.selectCate5("品牌", "LANCOME")
        
        #self.getJSON("json")
        #self.getWholeCate3("美妝個清", "臉部保養", "化妝水")
    

    
    #讓使用者選擇類別
    def showCategories(self):
        categories = self.category.getCategories("string")

        print("請選擇類別:")
        for c in range(len(categories)):
            print(str(c+1) + " " + categories[c])
        
        input01 = int(input()) - 1
        if(input01 in range(len(categories))):
            self.theCategory = categories[input01]

    #讓使用者選擇類別之下的大分類
    def showSubCate1(self):
        subCate1 = self.category.getSubCategories1(self.theCategory, "string")
        subCate1.pop()
        subCate1.append("結束選取，輸出JSON檔。")
        
        print("請選擇大分類:")
        for s in range(len(subCate1)):
            print(str(s+1) + " " + subCate1[s])
        
        input01 = int(input()) - 1
        
        if(input01 in range(len(subCate1) - 1)):
            self.theSubCate1 = subCate1[input01]
            self.showSubCate2()
        elif(input01 + 1 == len(subCate1)):
            self.getJSON("json")
        
    #讓使用者選擇大分類之下的小分類
    def showSubCate2(self):
        subCate2 = self.category.getSubCategories2(self.theSubCate1, "string")
        subCate2.append("結束選取")
        
        print("請選擇小分類:")
        for s in range(len(subCate2)):
            print(str(s+1) + " " + subCate2[s])
        input01 = int(input()) - 1
        if(input01 in range(len(subCate2) - 1)):
            self.theSubCate2.append(subCate2[input01])
            print("目前選取小分類:")
            print(self.theSubCate2)
            self.showSubCate1()
        elif(input01 + 1 == len(subCate2)):
            self.showSubCate1()
    
    def getWholeCate3(self, Cate0, Cate1, Cate2):
        self.theCate0 = Cate0
        self.theCate1 = Cate1
        self.theCate2 = Cate2

        self.category.goToCate2(Cate0, Cate1, Cate2)
        Cate3 = self.category.getCate3List("string")
        for c in Cate3:
            #每次都要初始化
            self.__init__()
            
            print("開始蒐集Cate3 " + c + "\n")
            self.theCate0 = Cate0
            self.theCate1 = Cate1
            self.theCate2 = Cate2
            self.theCate3 = c
            self.category.goToCate3Link(c)
            self.getJSON("json")
            
            
    def getJSON(self, outType):
        def write_json(json, fileName):
            with open("%s.json" % (fileName), mode = "w", encoding = "utf-8") as file:
                file.write(json)
                
        
        productLinkList = self.category.getProductsLinksList()
        print(productLinkList)
        print("已選取商品數: %d\n" % len(productLinkList))
        
        out = {}
        out.update({"總數量": ""})
        out.update({"Cate0": ""})
        out.update({"Cate1": ""})
        out.update({"Cate2": ""})
        out.update({"Cate3": ""})
        out.update({"Cate4": ""})
        out.update({"Cate5": ""})
        out["總數量"] = len(productLinkList)
        out["Cate0"] = self.theCate0
        out["Cate1"] = self.theCate1
        out["Cate2"] = self.theCate2
        out["Cate3"] = self.theCate3
        out["Cate4"] = self.theCate4
        Cate5Str = ""
        for i in self.theCate5:
            Cate5Str = Cate5Str + " " + i
        out["Cate5"] = Cate5Str
        out.update({"商品訊息列表": []})
        
        print("開始抓取商品資訊...\n")
        count = 1
        for p in productLinkList:
            link = p[0]
            try:
                productInfo = self.product.getProductInfo(link)
                out["商品訊息列表"].append(productInfo)
                print("已抓取商品資訊: " + str(count) + " / " + str(len(productLinkList)) + " 個")
                count += 1
            except:
                print("errorLink: " + link)
        print("商品資訊抓取完成，儲存/回傳中...\n")    
        json_formatted_str = json.dumps(out, ensure_ascii = False, indent=2)
        if(outType == "json"):
            fileName = self.theCate0 + " " + self.theCate1 + " " + self.theCate2 + " " + self.theCate3 
            write_json(json_formatted_str, fileName)
            print("商品資訊儲存完成。\n")
        elif(outType == "return"):
            print("商品資訊回傳完成。\n")
            return json_formatted_str
        
        
    
m = Main()
m.getWholeCate3("美妝個清", "臉部保養", "化妝水")
