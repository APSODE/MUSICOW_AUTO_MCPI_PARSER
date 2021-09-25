from selenium import webdriver
import urllib.request as URLRQ
from PIL import Image

from Class.USER_JSON_RW.rw_json import READ_WRITE
import random, sys, os, time, datetime, json, discord

GRAPH_SCREENSHOT_FILE = "GRAPH_SCREENSHOT.png"
MAIN_CONFIG_DIR = ".\\MAIN_CONFIG\\MAIN_CONFIG.json"
CLASS_CONFIG_DIR = ".\\Class\\AUTO_DATA_REFRESH\\AUTO_DATA_REFRESH_CONFIG\\AUTO_DATA_REFRESH_CONFIG.json"
MCPI_VALUE_SAVEFILE = ".\\Class\\AUTO_DATA_REFRESH\\MCPI_VALUE_SAVEFILE.json"
CH_DRIVER_DIR = ".\\chromedriver_win32\\chromedriver.exe"

UTF_8_ENCODING = "utf-8"
WRITE_MODE = "w"

class INTERNAL_FUNC:
    def Del(Second = 1):
        time.sleep(Second)
        return Second

    def Driver_Get_X_Path(XPath, DRIVER):
        time.sleep(0.5)
        driver = DRIVER
        dgxp = driver.find_element_by_xpath(XPath)
        return dgxp
    def Driver_Get_Class(ClassName, driver):
        try:
            dgc = driver.find_element_by_class_name(ClassName)
            return dgc
        except:
            del_sec = 1.5
            time.sleep(del_sec + 5.5) #로딩이 느려 예외가 발생했을 경우 5초 delay를 주어 대기후 다시 코드 시작
            dgc = driver.find_element_by_class_name(ClassName)
            return dgc    
    def Driver_Get_CSS(CSS_SELECTOR, driver):
        time.sleep(1)
        dgcs = driver.find_element_by_css_selector(CSS_SELECTOR)
        return dgcs








class AUTO_REFRESH:
    def TIME_CHECK(TEST_RUN = False):
        READ_CONFIG_DATA = READ_WRITE.READ_JSON(MAIN_CONFIG_DIR)
        BASETIME_DATA = READ_CONFIG_DATA["BASETIME_DATA"]
        # BASETIME_HOUR = BASETIME_DATA["HOUR"]
        BASETIME_MIN = BASETIME_DATA["MIN"]
        BASETIME_SEC = BASETIME_DATA["SEC"]

        TODAY = datetime.datetime.today()
        # TD_HOUR = TODAY.hour
        TD_MIN = TODAY.minute
        TD_SEC = TODAY.second

        if TEST_RUN == False:
            if (TD_MIN % BASETIME_MIN) == 0:
                if TD_SEC == BASETIME_SEC:
                    return True  
                else:
                    return False
            else:
                return False

        elif TEST_RUN == True:
            return True
            

        





    def REFRESH_DATA(TIME_CHECK, TEST_RUN = False):
        if TIME_CHECK == True or TEST_RUN == True:
            READ_CONFIG_DATA = READ_WRITE.READ_JSON(CLASS_CONFIG_DIR)
            MCPI_INDEX_SITE = READ_CONFIG_DATA["SITE_URL_LIST"]["MCPI_INDEX_SITE"]
            MCPI_XPATH_DATA = READ_CONFIG_DATA["MCPI_INDEX_XPATH"]

            MCPI_CURRENT_VALUE_XPATH = MCPI_XPATH_DATA["MCPI_CURRENT_VALUE"]
            MCPI_FLUCTUATE_AMOUNT_XPATH = MCPI_XPATH_DATA["MCPI_FLUCTUATE_AMOUNT"]
            MCPI_FLUCTUATE_PERCENTAGE_XPATH = MCPI_XPATH_DATA["MCPI_FLUCTUATE_PERCENTAGE"]

            TODAY = datetime.datetime.today()
            TODAY_DATA = str(TODAY).split(" ")[0]
            TIME_DATA = f"{TODAY.hour} : {TODAY.minute} : {TODAY.second}"


            
            GRAPH_XPATH = READ_CONFIG_DATA["GRAPH_XPATH"]

            OPTION = webdriver.ChromeOptions()
            # OPTION.add_argument("headless")
            # OPTION.add_argument("--start-maximized")
            
            # WEBDRIVER = webdriver.Chrome(CH_DRIVER_DIR, options = OPTION)
            

            WEBDRIVER = webdriver.Chrome(CH_DRIVER_DIR)
            WEBDRIVER.get(MCPI_INDEX_SITE)
            WEBDRIVER.save_screenshot(GRAPH_SCREENSHOT_FILE)
            WEBDRIVER.implicitly_wait(time_to_wait = 5)

            MCPI_CURRENT_VALUE = INTERNAL_FUNC.Driver_Get_X_Path(XPath = MCPI_CURRENT_VALUE_XPATH, DRIVER = WEBDRIVER).text
            MCPI_FLUCTUATE_AMOUNT = INTERNAL_FUNC.Driver_Get_X_Path(XPath = MCPI_FLUCTUATE_AMOUNT_XPATH, DRIVER = WEBDRIVER).text
            MCPI_FLUCTUATE_PERCENTAGE = INTERNAL_FUNC.Driver_Get_X_Path(XPath = MCPI_FLUCTUATE_PERCENTAGE_XPATH, DRIVER = WEBDRIVER).text

            GRAPH = INTERNAL_FUNC.Driver_Get_X_Path(XPath = GRAPH_XPATH, DRIVER = WEBDRIVER)
            GRAPH_LOCATION = GRAPH.location
            # GRAPH_SIZE = GRAPH.size

            IMG = Image.open(GRAPH_SCREENSHOT_FILE)
            GRAPH_LEFT = GRAPH_LOCATION["x"] - 10
            GRAPH_TOP = GRAPH_LOCATION["y"]
            GRAPH_RIGHT = GRAPH_LOCATION["x"] + 950
            GRAPH_BUTTOM = GRAPH_LOCATION["y"] + 422.66 #HEIGHT = 422.66

            try:
                if TEST_RUN == True:
                    print((GRAPH_LEFT, GRAPH_TOP, GRAPH_RIGHT, GRAPH_BUTTOM))

                IMG = IMG.crop((GRAPH_LEFT, GRAPH_TOP, GRAPH_RIGHT, GRAPH_BUTTOM))
                IMG.save(GRAPH_SCREENSHOT_FILE)
                RT_FILE = discord.File(GRAPH_SCREENSHOT_FILE)
            except Exception as ERROR_TYPE:
                RT_ERROR_MSG = f"### ERROR NOTICE ###\n\n{ERROR_TYPE}\n\n\n### ERROR INFO ###\n\nGRAPH_LOCATION = {GRAPH_LOCATION}\nGRAPH_LEFT = {GRAPH_LEFT}\nGRAPH_TOP = {GRAPH_TOP}\nGRAPH_RIGHT = {GRAPH_RIGHT}\nGRAPH_BUTTOM = {GRAPH_BUTTOM}"
                return RT_ERROR_MSG

            finally:
                WEBDRIVER.quit()

            
        
            READ_SAVEFILE_DATA = READ_WRITE.READ_JSON(MCPI_VALUE_SAVEFILE)
            with open(MCPI_VALUE_SAVEFILE, WRITE_MODE, encoding = UTF_8_ENCODING) as WRITE_SAVEFILE_PROFILE:
                if TODAY_DATA not in [F_KEY for F_KEY in READ_SAVEFILE_DATA]:    
                    READ_SAVEFILE_DATA[TODAY_DATA] = {}
                if TIME_DATA not in [S_KEY for S_KEY in READ_SAVEFILE_DATA[TODAY_DATA]]:    
                    READ_SAVEFILE_DATA[TODAY_DATA][TIME_DATA] = {}
                    
                READ_SAVEFILE_DATA[TODAY_DATA][TIME_DATA]["MCPI_CURRENT_VALUE"] = MCPI_CURRENT_VALUE
                READ_SAVEFILE_DATA[TODAY_DATA][TIME_DATA]["MCPI_FLUCTUATE_AMOUNT"] = MCPI_FLUCTUATE_AMOUNT
                READ_SAVEFILE_DATA[TODAY_DATA][TIME_DATA]["MCPI_FLUCTUATE_PERCENTAGE"] = MCPI_FLUCTUATE_PERCENTAGE
                json.dump(READ_SAVEFILE_DATA, WRITE_SAVEFILE_PROFILE, indent = 4)
            if TEST_RUN != True:
                return RT_FILE
        else:
            False
    def CURRENT_MCPI_DATA():
        READ_SAVEFILE_DATA = READ_WRITE.READ_JSON(MCPI_VALUE_SAVEFILE)
        F_KEY_LIST = [F_KEY for F_KEY in READ_SAVEFILE_DATA]
        F_KEY_LIST_LAST_INDEX = len(F_KEY_LIST) - 1
        F_KEY_NAME = F_KEY_LIST[F_KEY_LIST_LAST_INDEX]

        S_KEY_LIST = [S_KEY for S_KEY in READ_SAVEFILE_DATA[F_KEY_NAME]]
        S_KEY_LIST_LAST_INDEX = len(S_KEY_LIST) - 1
        S_KEY_NAME = S_KEY_LIST[S_KEY_LIST_LAST_INDEX]

        MCPI_CURRENT_VALUE = READ_SAVEFILE_DATA[F_KEY_NAME][S_KEY_NAME]["MCPI_CURRENT_VALUE"] 
        MCPI_FLUCTUATE_AMOUNT = READ_SAVEFILE_DATA[F_KEY_NAME][S_KEY_NAME]["MCPI_FLUCTUATE_AMOUNT"]
        MCPI_FLUCTUATE_PERCENTAGE = READ_SAVEFILE_DATA[F_KEY_NAME][S_KEY_NAME]["MCPI_FLUCTUATE_PERCENTAGE"]

        MCPI_UP_DOWN_EMOJI_LIST = [":chart_with_upwards_trend:", ":chart_with_downwards_trend:"]
        if "+" in MCPI_FLUCTUATE_PERCENTAGE:
            USE_EMOJI = MCPI_UP_DOWN_EMOJI_LIST[0]
        elif "-" in MCPI_FLUCTUATE_PERCENTAGE:
            USE_EMOJI = MCPI_UP_DOWN_EMOJI_LIST[1]

        RT_EMBED = discord.Embed(title = ":bar_chart: 현재의 MCPI지수 :bar_chart:", description = "")
        RT_EMBED.add_field(name = ":scroll: 현재 MCPI지수 :scroll:", value = MCPI_CURRENT_VALUE, inline = False)
        RT_EMBED.add_field(name = f"{USE_EMOJI} 현재 MCPI지수 상승폭 {USE_EMOJI}", value = f"{MCPI_FLUCTUATE_AMOUNT}\n", inline = False)
        RT_EMBED.add_field(name = f"{USE_EMOJI} 현재 MCPI지수 상승퍼센트 {USE_EMOJI}", value = f"{MCPI_FLUCTUATE_PERCENTAGE}\n", inline = False)

        return RT_EMBED



if __name__ == "__main__":
    AUTO_REFRESH.REFRESH_DATA(TIME_CHECK = True, TEST_RUN = True)
    
    