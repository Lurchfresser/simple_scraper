from seleniumbase import SB
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from dateutil import parser
from seleniumbase.undetected.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

navHeight = 0


def get_shadow_root(element,sb):
    return sb.execute_script('return arguments[0].shadowRoot', element)

def get_slot(element,sb):
    return sb.execute_script('return arguments[0].parentElement.shadowRoot.querySelector(`slot[name="${arguments[0].slot}"]`)', element)

def get_first_comment_parent(element, sb):
    try:
        parent = element.find_element(By.XPATH, 'ancestor::shreddit-comment')
        return parent
    except:
        return None

def is_pressable(svg,sb,ancestor_test):
        try:
            if (svg.size["height"] == 0 or svg.size["width"] == 0):
                return False
            if (svg.get_attribute("style").find("display: none") != -1):
                return False
            if (svg.get_attribute("style").find("visibility: hidden") != -1):
                return False
            #discard more buttons that would lead to new pages
            parent_comment = get_first_comment_parent(svg,sb)
            if (parent_comment is not None):
                if (int(parent_comment.get_attribute("depth")) > 3):
                    return False
            if (not svg.is_displayed()):
                return False
            try:
                loading_button = svg.find_element(By.CSS_SELECTOR, 'icon-load')
                if (loading_button.size["height"] != 0 and loading_button.size["width"] != 0):
                    return False
            except:
                pass
            if (ancestor_test(svg,sb) == False):
                return False
            #get element at the coordinates of the element
            # Calculate center coordinates of the element
            rect = svg.rect
            center_x = rect['x'] + rect['width'] / 2
            center_y = rect['y'] + rect['height'] / 2
            try:
                #scroll to the element
                sb.execute_script("arguments[0].scrollIntoView();", svg)
                # Calculate center coordinates of the element (global)
                rect = svg.rect
                center_x = rect['x'] + rect['width'] / 2
                center_y = rect['y'] + rect['height'] / 2
                
                # Get the element at the adjusted center coordinates
                center_element = sb.execute_script(
                    "return document.elementFromPoint(arguments[0], arguments[1]);",
                    center_x, center_y
                )
                if (center_element is not None and center_element.tag_name != "path" and center_element.tag_name != "svg"):
                    return False
            except Exception as e:
                print(e)
            return True
        except Exception as e:
            return False

def has_faceplate_ancestor(element,sb):
    try:
        faceplate = element.find_element(By.XPATH, 'ancestor::faceplate-partial')
        return True
    except:
        return False
    
def has_button_ancestor(element,sb):
    try:
        button = element.find_element(By.XPATH, 'ancestor::button')
        return True
    except:
        return False
    

def press_more_buttons(root_comment: WebElement, sb):
    while True:
        commentsEmpty = False
        more_buttons_empty = False
        comments = root_comment.find_elements(By.CSS_SELECTOR, 'shreddit-comment')
        for comment in comments:
            comment_more_buttons = comment.shadow_root.find_elements(By.CSS_SELECTOR, 'svg[icon-name="join-outline"]')
            comment_more_buttons = [button for button in comment_more_buttons if is_pressable(button,sb,has_button_ancestor)]
            for button in comment_more_buttons:
                try:
                    html_button = button.find_element(By.XPATH, 'ancestor::button')
                    sb.execute_script("arguments[0].scrollIntoView();", html_button)
                    sb.execute_script("window.scrollBy(0, -arguments[1] * 1.5);", html_button, navHeight)
                    html_button.uc_click()
                except Exception as e:
                    if (e is not NoSuchElementException()):
                        print("Error: ", e)
        more_buttons = root_comment.find_elements(By.CSS_SELECTOR, 'svg[icon-name="join-outline"]')
        more_buttons = [button for button in more_buttons if is_pressable(button,sb,has_faceplate_ancestor)]
        more_buttons_length = len(more_buttons)
        catches = 0
        if (more_buttons_length == 0):
            return
        for button in more_buttons:
            try:
                faceplate = button.find_element(By.XPATH, 'ancestor::faceplate-partial')
                sb.execute_script("arguments[0].scrollIntoView();", faceplate)
                sb.execute_script("window.scrollBy(0, -arguments[1] * 1.5);", faceplate, navHeight)
                faceplate.uc_click()
            except Exception as e:
                print("Error: ", e)
                catches += 1
        if (catches == more_buttons_length):
            return

def getIndex(l,id):
    try:
        for (i,elem) in enumerate(l):
            if elem.get_attribute("thingid") == id:
                return i + 1
    except:
        return 0
    return 0


#TODO: implement logic for [deleted]
def extraction(elem,sb):
    try:
        info_div = elem.find_element(By.CSS_SELECTOR, 'div[slot="commentMeta"]')
        user_name = info_div.find_element(By.CSS_SELECTOR, 'a').text
        print("User: ", user_name)
        time = info_div.find_element(By.CSS_SELECTOR, 'time').get_attribute("datetime")
        date_obj = parser.parse(time)
        print("Time: ", date_obj)
        id = elem.get_attribute("thingid")
        print("ID: ", id)
        text = elem.find_element(By.ID, f'{id}-comment-rtjson-content').text
        print("Text: ", text)
        #TODO: later catch errors
        reddit_depth = int(elem.get_attribute("depth"))
        if (reddit_depth >= 1):
            parent_id = elem.get_attribute("parentid")
            print("Parent ID: ", parent_id)
        else:
            print("Parent ID: None")
        content_type = elem.get_attribute("content-type")
        print("Content Type: ", content_type)
        press_more_buttons(elem,sb)
        children = elem.find_elements(By.XPATH, './shreddit-comment')
        for child in children:
            extraction(child,sb)
        print("--------------------------------------------------")
        #TODO: implement logic for [deleted], (throws error here) and other error sources
    except Exception as e:
        print("Error: ", e)
        return

#/bin/brave-browser       chromium_arg="--tor"
#/home/lurchfresser/Downloads/ungoogled-chromium_125.0.6422.76-1_linux/chrome
#with SB(uc=True, binary_location="/home/lurchfresser/Downloads/ungoogled-chromium_125.0.6422.76-1_linux/chrome", headed=True, demo=True) as sb:

with SB(uc=True, binary_location="/home/lurchfresser/Downloads/ungoogled-chromium_125.0.6422.76-1_linux/chrome", headed=True, demo=True) as sb:
    url = 'https://www.reddit.com/r/AskReddit/comments/1dg65qq/which_movie_in_your_opinion_is_the_saddest_movie/'
    sb.open(url)
    length = 0
    last_id = ""
    nav = sb.find_element(By.CSS_SELECTOR, 'nav')
    navHeight = nav.size["height"]
    while True:
        shreddit_comments = sb.find_elements(By.CSS_SELECTOR, 'shreddit-comment-tree > shreddit-comment')
        index = getIndex(shreddit_comments,last_id)
        for elem in shreddit_comments[index:]:
            press_more_buttons(elem,sb)
            extraction(elem, sb)
            break
        length = len(shreddit_comments)
        last_id = shreddit_comments[-1].get_attribute("thingid")
        print("length: ", length)
        sb.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #TODO: Better await conditions, takes sometimes longer than timeout
        try:
            sb.uc_click("shreddit-comment-tree > faceplate-partial:contains('View more comments')")
        except:
            print("StaleElementReferenceException")
            break
    sb.driver.quit()

        