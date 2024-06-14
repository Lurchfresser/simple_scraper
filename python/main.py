from seleniumbase import SB
import re
from dateutil import parser
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase.common.exceptions import NoSuchElementException as SBNoSuchElementException

def get_shadow_root(element,sb):
    return sb.execute_script('return arguments[0].shadowRoot', element)


def extractInfos(elem,sb):
    href = elem.get_attribute("href")
    print("link: ",href)
    text = elem.text
    try:
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
        print(date_obj)
    except NoSuchElementException as e:
        print("Faceplate number element not found. This might not be an error depending on the page structure.")
    except Exception as e:
        print("An unexpected error occurred:", e) 
    


with SB(uc=True, binary_location="/home/lurchfresser/Downloads/ungoogled-chromium_125.0.6422.76-1_linux/chrome", headed=True) as sb:
    #url = "https://www.reddit.com/user/CryptoDaily-/"
    url = 'https://www.reddit.com/r/CryptoCurrency/new/'
    sb.driver.uc_open_with_reconnect(url, 3)
    length = 0
    lenForScroll = 0
    while True:
        elems = sb.find_elements("shreddit-post")
        print("length: ",len(elems))
        for elem in elems[length:]:
            extractInfos(elem,sb=sb)
        length = len(elems)
        lenForScroll = len(sb.find_elements("shreddit-feed > *"))
        try:
            print("length for scroll: ",lenForScroll)
            sb.scroll_to(f"shreddit-feed > *:nth-child({lenForScroll})")
        except SBNoSuchElementException as e:
            print("No more elements to wait for.")
            break
        try:
            sb.wait_for_query_selector(f"shreddit-feed > *:nth-child({lenForScroll+1})")
        except NoSuchElementException as e:
            print("No more elements to scroll to.")
            break
    print("Done")
    #sb.driver.quit()
    sb.wait(1000)
    #main-content > div:nth-child(3) > shreddit-feed > faceplate-batch:nth-child(22) > article:nth-child(9)
