from seleniumbase import SB
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException


with SB(uc=True, binary_location="/home/lurchfresser/Downloads/ungoogled-chromium_125.0.6422.76-1_linux/chrome", headed=True) as sb:
    url = 'https://www.reddit.com/r/AskReddit/comments/1dg65qq/which_movie_in_your_opinion_is_the_saddest_movie/'
    sb.open(url)
    length = 0
    while True:
        shreddit_comments = sb.find_elements(By.CSS_SELECTOR, 'shreddit-comment')
        length = len(shreddit_comments)
        print("length: ", length)
        sb.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #TODO: Better await conditions, takes sometimes longer than timeout
        try:
            sb.uc_click("shreddit-comment-tree > faceplate-partial")
        except:
            print("StaleElementReferenceException")
            continue

        