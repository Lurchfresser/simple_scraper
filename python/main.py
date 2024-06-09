from seleniumbase import SB
import re
from datetime import datetime

def extractInfos(elem):
    href = elem.get_attribute("href")
    print(href)
    text = elem.text
    pattern = r"(\w+ \d{1,2}, \d{4})"
    match = re.search(pattern, text)
    if match:
        date_str = match.group(1)
        date_obj = datetime.strptime(date_str, "%B %d, %Y")
        print(date_obj)
    else:
        print("No date found in the text.")


with SB(uc=True, demo=True, binary_location="/home/lurchfresser/Downloads/ungoogled-chromium_125.0.6422.76-1_linux/chrome", headed=True) as sb:
    url = "https://www.reddit.com/user/CryptoDaily-/"
    sb.driver.uc_open_with_reconnect(url, 3)
    length = 0
    while True:
        elems = sb.find_elements("article a.absolute.inset-0")
        print(len(elems))
        if length == len(elems):
            print("No more elements")
            break
        for elem in elems[length:]:
            extractInfos(elem)
        length = len(elems)
        sb.scroll_to_bottom()
        sb.wait(7)
    sb.driver.quit()