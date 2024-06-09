from seleniumbase import SB

with SB(uc=True, demo=True, binary_location="/home/lurchfresser/Downloads/ungoogled-chromium_125.0.6422.76-1_linux/chrome", headed=True) as sb:
    url = "https://www.reddit.com/user/CryptoDaily-/"
    sb.driver.uc_open_with_reconnect(url, 3)
    elems = sb.find_elements("#t3_1dd0k02 > a")
    print(elems.__len__())
    sb.scroll_to_bottom()
    sb.wait(3)
    elems = sb.find_elements("#t3_1dd0k02 > a")
    print(elems.__len__())
    sb.driver.quit()
    