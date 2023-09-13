import json
import Category, Product
import undetected_chromedriver as uc
from datetime import datetime

class Main():
    def __init__(self) -> None:
        def __get_ChromeOptions(): 
            options = uc.ChromeOptions()
            options.add_argument('--start_maximized')
            options.add_argument("--disable-extensions")
            options.add_argument('--disable-application-cache')
            options.add_argument('--disable-gpu')
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-notifications")
            options.add_argument("--incognito")
            
            options.add_argument("--disable-dev-shm-usage")
            # options.add_argument("--user-data-dir=C:\\Users\\v99sa\\Desktop\\coding\\py\\Momo_WebCrawler\\Momo_WebCrawler\\profile1")
            return options
        
        self.driver = uc.Chrome(browser_executable_path=r"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", options=__get_ChromeOptions())
        self.category = Category.Category(self.driver)
        self.product = Product.Product(self.driver, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.179 Safari/537.36')
        self.theCategory = ""
        self.theSubCate1 = ""
        self.theSubCate2 = []
        
        self.showCategories()
        self.showSubCate1()
    
    def showCategories(self):
        categories = self.category.getCategories("string")

        print("請選擇類別:")
        for c in range(len(categories)):
            print(str(c+1) + " " + categories[c])
        
        input01 = int(input()) - 1
        if(input01 in range(len(categories))):
            self.theCategory = categories[input01]

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
    
    def getJSON(self, outType):
        def write_json(folder_name, json, fileName):
            with open("./{}.json".format(fileName), mode = "w", encoding = "utf-8") as file:
                file.write(json)
                
        for s in self.theSubCate2:
            self.category.selectSubCate2(self.theSubCate1, s)
        productLinkList = self.category.getProductsLinksList()
        print("已選取商品數: %d" % len(productLinkList))
        out = {}
        out.update({"類別": ""})
        out.update({"大分類": ""})
        out["類別"] = self.theCategory
        out["大分類"] = self.theSubCate1
        subCate2Str = ""
        for i in self.theSubCate2:
            subCate2Str = subCate2Str + " " + i
        out.update({"小分類": ""})
        out["小分類"] = subCate2Str
        out.update({"商品訊息列表": []})
        
        for p in productLinkList:
            link = p[0]
            productInfo = self.product.getProductInfo(link)
            out["商品訊息列表"].append(productInfo)
            
        json_formatted_str = json.dumps(out, ensure_ascii = False, indent=2)
        if(outType == "json"):
            fileName = datetime.now().strftime("out")
            write_json("output", json_formatted_str, fileName)
        elif(outType == "return"):
            return json_formatted_str
         
    
m = Main()
m.getJSON()