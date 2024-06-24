from seleniumbase import SB

with SB(uc=True, binary_location="/home/lurchfresser/Downloads/ungoogled-chromium_125.0.6422.76-1_linux/chrome", headed=True) as sb:
    url = 'https://seleniumbase.io/coffee/'
    sb.driver.uc_open_with_reconnect(url, 3)
    elem = sb.find_element('h4')
    sb.highlight(elem, loops=40)
    sb.wait(100)    