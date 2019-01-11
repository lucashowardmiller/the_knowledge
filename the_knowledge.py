import sys
from selenium import webdriver
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
    # grab input
    subject_search = input('Enter a search: ')
    knowledge_panel_search = input('Use the knowledge panel from: ')
    hide_search_entry = input('Hide search (y/n): ')
    
    # check if hide_search_entry is affirmative
    hide_search = hide_search_entry.lower() == 'y'

    if hide_search:
        return_url = f'{GOOGLE_PREFIX}{whitespace_to_plus(subject_search)}&{get_knowledge_panel(knowledge_panel_search)}&{KP_ONLY}'
    else:
        return_url = f'{GOOGLE_PREFIX}{whitespace_to_plus(subject_search)}&{get_knowledge_panel(knowledge_panel_search)}'
    print(return_url)


def get_knowledge_panel(knowledge_panel_search: str) -> str:
    """Gets the knowledge panel short link corresponding with the user selection"""

    # sets up the driver
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(10)

    # searches google for the knowledge panel
    driver.get("https://google.com")
    search_box =  driver.find_element_by_xpath('/html/body/div/div[3]/form/div[2]/div/div[1]/div/div[1]/input')
    search_box.click()
    search_box.send_keys(knowledge_panel_search)
    search_box.send_keys(u'\ue007')

    # clicks on the share box of the knowledge panel and gets the short link
    try:
        kp_link = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div[10]/div[1]/div[3]/div/div/div[1]/div[1]/div/div[1]/div[2]/div[2]/div/div[1]/div/div/div[1]/kno-share-button/div/span')
        kp_link.click()
        short_kp = driver.find_element_by_xpath('/html/body/div[6]/div[1]/div/div[2]/div[2]/div/div/g-text-field/input')
        short_kp_link = short_kp.get_attribute('value')
    except:
        print("ERROR: No (compatible) knowledge panel was found.")
        sys.exit(1)

    # converts the short link to the long link by going to it
    driver.get(short_kp_link)
    full_kp_link = driver.current_url
    driver.quit()

    # extracts the knowledge panel link from the full url (ex. '&kgmid=/g/1210rwkh')
    url_split = full_kp_link.split('?')
    url_split = url_split[1].split('&')
    return url_split[0]


def whitespace_to_plus(search: str) -> str:
    """Handles making most strings safe to put into urls"""
    return '+'.join(search.split())


if __name__ == '__main__':
    print(main_art)
    main()
