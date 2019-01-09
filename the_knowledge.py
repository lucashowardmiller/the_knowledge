import time
import urllib.request
import urllib.parse
from selenium import webdriver
import re
from selenium.webdriver.firefox.options import Options

GOOGLE_PREFIX = 'https://www.google.com/search?q='
KP_ONLY = '&kponly'

main_art = \
    """___________.__              ____  __.                    .__             .___              
\__    ___/|  |__   ____   |    |/ _| ____   ______  _  _|  |   ____   __| _/ ____   ____  
  |    |   |  |  \_/ __ \  |      <  /    \ /  _ \ \/ \/ /  | _/ __ \ / __ | / ___\_/ __ \ 
  |    |   |   Y  \  ___/  |    |  \|   |  (  <_> )     /|  |_\  ___// /_/ |/ /_/  >  ___/ 
  |____|   |___|  /\___  > |____|__ \___|  /\____/ \/\_/ |____/\___  >____ |\___  / \___  >
                \/     \/          \/    \/                        \/     \/_____/      \/ """


def main():
    print('Enter a search:', end=' ')
    subject_search = input()
    print('Use the knowledge panel from:', end=' ')
    knowledge_panel_search = input()
    print('Hide search (y/n):', end=' ')
    hide_search_entry = input()
    if hide_search_entry.lower() == 'y':
        hide_search = True
    else:
        hide_search = False

    if hide_search:
        return_url = GOOGLE_PREFIX + whitespace_to_plus(subject_search)\
                     + '&' + get_knowledge_panel(knowledge_panel_search) + '&' + KP_ONLY
    else:
        return_url = GOOGLE_PREFIX + whitespace_to_plus(subject_search) + '&' + get_knowledge_panel(
            knowledge_panel_search)
    print(return_url)


def google_search_url():
    with urllib.request.urlopen('http://python.org/') as response:
        html = response.read()
        print(html)


def get_knowledge_panel(knowledge_panel_search: str) -> str:
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get("https://google.com")
    search_box = driver.find_element_by_xpath('/html/body/div/div[3]/form/div[2]/div/div[1]/div/div[1]/input')
    search_box.click()
    search_box.send_keys(knowledge_panel_search)
    search_box.send_keys(u'\ue007')

    time.sleep(2)
    kp_link = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div[10]/div[1]/div[3]/div/div/div[1]/div[1]/div/div[1]/div[2]/div[2]/div/div[1]/div/div/div[1]/kno-share-button/div/span')
    kp_link.click()
    short_kp = driver.find_element_by_xpath('/html/body/div[6]/div[1]/div/div[2]/div[2]/div/div/g-text-field/input')
    short_kp_link = short_kp.get_attribute('value')

    driver.get(short_kp_link)
    time.sleep(2)
    full_kp_link = driver.current_url
    driver.quit()
    url_split = full_kp_link.split('?')
    url_split = url_split[1].split('&')
    return url_split[0]


def whitespace_to_plus(search: str) -> str:
    """Handles making most strings safe to put into urls"""
    whitespace_re = re.compile('\s')
    return re.sub(whitespace_re, '+', search)


if __name__ == '__main__':
    print(main_art)
    main()



