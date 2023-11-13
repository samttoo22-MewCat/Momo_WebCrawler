import json
import os
import Modules.CategoryHandler as CategoryHandler, Modules.ProductHandler as ProductHandler
import undetected_chromedriver as uc
from datetime import datetime
import asyncio
import datetime
from datetime import datetime
import traceback
import sys
from selenium.webdriver.common.by import By

class Main():
    def __init__(self) -> None:
        self.browser_executable_path = "C:\\Users\\v99sa\\Desktop\\chrome-win\\chrome.exe"
        self.driver = uc.Chrome(browser_executable_path=r"%s" % self.browser_executable_path, options=self.__get_ChromeOptions(), version_main=110)
        self.categoryHandler = CategoryHandler.Handler(self.driver)
        self.productHandler = ProductHandler.Handler(self.driver, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
        self.lock = asyncio.Lock()

        #測試區

        #print(self.categoryHandler.getCate2List("美妝個清", "香氛/SPA", "string"))
        #self.categoryHandler.goToCate2Link("美妝個清", "香氛/SPA", "精油/擴香")
        #print(self.categoryHandler.getCate3List("string"))
        #self.categoryHandler.goToCate3Link("女香")
        #print(self.categoryHandler.getProductsLinksList())
        
        #self.categoryHandler.goToCate3Link("精華液")
        #self.categoryHandler.selectCate5("品牌", "LANCOME")

        #測試區
        
    #瀏覽器設定
    def __get_ChromeOptions(self): 
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

    async def getWholeCate3Products(self, Cate0, Cate1, Cate2):

        self.categoryHandler.goToCate2Link(Cate0, Cate1, Cate2)
        Cate3List = self.categoryHandler.getCate3List("string")
        print(Cate3List)
        
        print("找到 " + str(len(Cate3List)) + " 個 Cate3，開始抓取。")
        def create_folder(folder_name):
                if not os.path.exists("./%s" % folder_name): 
                    os.mkdir("./%s" % folder_name)
                    print("未找到 ./%s 資料夾，已自動創建。" % folder_name)
                else:
                    print("找到輸出資料夾./out。")
        create_folder("out")
        async def getSingleCate3Products(Cate3):

            newDriver = uc.Chrome(browser_executable_path=self.browser_executable_path, options=self.__get_ChromeOptions(), version_main=110)
            newCategoryHandler = CategoryHandler.Handler(newDriver)
            newProductHandler = ProductHandler.Handler(newDriver, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
            time_start = datetime.now()
            time_start_str = time_start.strftime("%m/%d/%Y, %H:%M:%S")
            time_end = datetime.now()

            
            def write_json(folder_name, dict, fileName):
                with open("./{}/{}.json".format(folder_name, fileName), mode = "w", encoding = "utf-8") as file:
                    json_str = json.dumps(dict, ensure_ascii=False, indent=2)
                    file.write(json_str)

            async def getCate3JSON(outType, Cate3):
                productLinkList = await asyncio.to_thread(newCategoryHandler.getProductsLinksList)
                print("已選取商品數: %d\n" % len(productLinkList))

                #輸出格式整理
                out = {}
                out.update({"總數量": len(productLinkList)})
                out.update({"開始抓取資料時間": time_start_str})
                out.update({"結束抓取資料時間": ""})
                out.update({"抓取資料所花的時間": ""})
                out.update({"Cate0": Cate0})
                out.update({"Cate1": Cate1})
                out.update({"Cate2": Cate2})
                out.update({"Cate3": Cate3})
                out.update({"Cate4": ""})
                out.update({"Cate5": ""})
                Cate5Str = ""

                out["Cate5"] = Cate5Str
                out.update({"商品訊息列表": []})

                print("開始抓取商品資訊...\n")
                count = 1
                for p in productLinkList:
                    link = p[0]
                    try:
                        productInfo = await asyncio.to_thread(newProductHandler.getProductInfo, link)
                        await asyncio.to_thread(out["商品訊息列表"].append, productInfo)
                        
                        print("已抓取商品資訊: " + str(count) + " / " + str(len(productLinkList)) + " 個")
                        count += 1
                    except Exception as e:
                        print(traceback.format_exc())
                        print("errorLink: " + link)

                print("商品資訊抓取完成，儲存/回傳中...\n")    
                time_end = datetime.now()
                time_end_str = time_end.strftime("%m/%d/%Y, %H:%M:%S")
                time_passed = time_end - time_start
                time_passed_str =  str(time_passed.seconds) + "秒"
                out["結束抓取資料時間"] = time_end_str
                out["抓取資料所花的時間"] = time_passed_str

                if(outType == "json"):
                    fileName = Cate0 + " " + Cate1 + " " + Cate2 + " " + Cate3
                    if("/" in fileName):
                        fileName = fileName.replace("/", "-")
                    async with self.lock:
                        await asyncio.to_thread(write_json, "out", out, fileName)
                    print("商品資訊儲存完成。\n")
                elif(outType == "return"):
                    print("商品資訊回傳完成。\n")
                    return out

            await asyncio.to_thread(newCategoryHandler.goToCate2Link, Cate0, Cate1, Cate2)
            await asyncio.to_thread(newCategoryHandler.goToCate3Link, Cate3)

            print("開始蒐集Cate3 " + Cate3 + "\n")
            await getCate3JSON("json", Cate3)

            newDriver.quit()
        sema = asyncio.Semaphore(value=10)

        tasks = []
        for c in Cate3List:
            if(Cate3List.index(c) <= 5):
            #async with sema:
                task = asyncio.create_task(getSingleCate3Products(c))
                tasks.append(task)

        await asyncio.gather(*tasks)

    def debugLink(self, link):
        self.productHandler.getProductInfo(link)



if __name__ == '__main__':          
    m = Main()

    asyncio.run(m.getWholeCate3Products("美妝個清", "香氛/SPA", "精油/擴香"))

    #m.debugLink("https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=10592219&str_category_code=1111700001&sourcePageType=4")