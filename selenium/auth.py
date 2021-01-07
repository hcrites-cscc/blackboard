#--- Configure:
#--- 1. Assign my_domain (see line 10)
#--- 2. Assign user_id (see line 13)
#--- 3. Assign user_password (see line 14)
#--- 4. Update Chrome profile path (--user-data-dir) (see line 28)
#--- 5. Update chromedriver.exe path (executable_path)  (see line 37)
#--- 6. Update code for entering username and password (see line 42-47)

# Set your domain here
my_domain = ""

# Set your username and password here
user_id = ""
user_password = ""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

def login():
    # Pulls up the course manager
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--ignore-certificate-errors-spki-list")
    chrome_options.add_argument("--user-data-dir=")
    chrome_options.add_argument("--profile-directory=selenium_profile")
    

    # Load AdBlock
    # path_to_extension = r""
    # options.add_argument("load-extension="+path_to_extension)

    # Initiate Driver
    driver = webdriver.Chrome(executable_path="", options=chrome_options)

    # Load Login Page
    driver.get(my_domain+"/webapps/login/")

    # This works on our custom login page, but may not work on your institution's page.  In short, you want to enter the username and password into the appropriate fields and submit them.
    if find_element_by_id(driver, "bb_access"):
        driver.find_element_by_id("bb_access").click() #-- Click a custom button
        driver.find_element_by_id("check_training").send_keys(user_id+Keys.ENTER) #-- Enter username and the ENTER key
        driver.find_element_by_name("password").send_keys(user_password) #-- Enter password
        driver.find_element_by_id("entry-login").click() #-- Click custom submit button

    print("=================\nLog In\n=================")

    return driver

def logout(driver):
    # Logout
    driver.find_element_by_id("topframe.logout.label").click()

    # Wait
    time.sleep(2)

    # Close windows
    windows = driver.window_handles
    for w in windows:
        driver.switch_to.window(w)
        driver.close()
    
    # Quit Browser
    driver.quit()

    print("=================\nLog Out\n=================")

def find_element_by_id(driver, element_id):
    try:
        driver.find_element_by_id(element_id)
    except NoSuchElementException:
        return False
    return True
