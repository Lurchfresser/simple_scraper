from seleniumbase import SB
import re
from dateutil import parser
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase.common.exceptions import NoSuchElementException as SBNoSuchElementException

def getIndex(l,id):
    try:
        for (i,elem) in enumerate(l):
            if elem.get_property("id") == id:
                return i + 1
    except:
        return 0
    return 0

def get_shadow_root(element,sb):
    return sb.execute_script('return arguments[0].shadowRoot', element)


def extractInfos(elem,sb):
    try:
        href = elem.find_element(By.CSS_SELECTOR,'a:first-of-type').get_attribute("href")
        print("link: ",href)
        user_elem = elem.find_element(By.CSS_SELECTOR,'faceplate-hovercard > faceplate-tracker > a > span:nth-of-type(2)')
        user_text = user_elem.text.split("u/")[1]
        print("User: ",user_text)
        shadow_root = get_shadow_root(elem, sb)
        faceplate_elems = shadow_root.find_elements(By.CSS_SELECTOR, 'faceplate-number')
        #comments_elem = shadow_root.find_element(By.XPATH, 'faceplate-number')
        if faceplate_elems:
            print("Likes:", faceplate_elems[0].get_attribute("number"))
            print("Comments:", faceplate_elems[1].get_attribute("number"))
        else:
            print("Faceplate number element not found.")
        timeElem = elem.find_element(By.XPATH,"..//time")
        time = timeElem.get_attribute("datetime")
        date_obj = parser.parse(time)
        topic = elem.find_element(By.CLASS_NAME,'flair-content').text
        print("Topic: ",topic)
        print(date_obj)
    except NoSuchElementException as e:
        print("Faceplate number element not found. This might not be an error depending on the page structure.")
    except Exception as e:
        print("An unexpected error occurred:", e) 
    print("--------------------------------------------------")
    


with SB(uc=True, binary_location="/home/lurchfresser/Downloads/ungoogled-chromium_125.0.6422.76-1_linux/chrome", headed=True) as sb:
    #url = "https://www.reddit.com/user/CryptoDaily-/"
    url = 'https://www.reddit.com/r/CryptoCurrency/new/'
    sb.driver.uc_open_with_reconnect(url, 3)
    length = 0
    last_id = ""
    lenForScroll = 0
    while True:
        elems = sb.find_elements(By.TAG_NAME,"shreddit-post")
        print("length: ",len(elems))
        index = getIndex(elems,last_id)
        for elem in elems[index:]:
            extractInfos(elem,sb=sb)
        lenForScroll = len(sb.find_elements("shreddit-feed > *"))
        last_id = elems[-1].get_property("id")
        #TODO: it still needs one iteration
        try:
            print("length for scroll: ",lenForScroll)
            #sb.scroll_to(f"shreddit-feed > *:nth-child({lenForScroll})")
            sb.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except SBNoSuchElementException as e:
            print("No more elements to scroll to")
            break
        try:
            sb.wait_for_query_selector(f"shreddit-feed > *:nth-child({lenForScroll+1})", timeout=20)
        except NoSuchElementException as e:
            print("No more elements to wait for.")
    print("Done")
    #sb.driver.quit()
    sb.wait(1000)
    #main-content > div:nth-child(3) > shreddit-feed > faceplate-batch:nth-child(22) > article:nth-child(9)
