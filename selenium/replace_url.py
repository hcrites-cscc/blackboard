from auth import *
import time, re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def replace_content(driver):
    global content_handlers
    with open('replace_url.txt', 'r') as replace_list:
        content_line = replace_list.read().splitlines()
        for content in content_line:
            course_id, content_id, replace_content = content.split("\t")    

            driver.get(my_domain+"/webapps/blackboard/execute/manageCourseItem?content_id=_"+content_id+"_1&course_id=_"+course_id+"_1&dispatch=edit&type=externallink")

            driver.find_element_by_id("url").clear()
            driver.find_element_by_id("url").send_keys(replace_content)

            driver.execute_script("document.getElementById('launchInNew_true').checked = true;")

            driver.find_element_by_name("bottom_Submit").click()
            driver.implicitly_wait(3)

            try:
                driver.find_element_by_id("goodMsg1").text
				print("Success: "+course_id+" "+content_id)
				
            except :
                print("Failed to update: "+course_id+" "+content_id)
                driver.implicitly_wait(3)

def main():
    driver = login()
    replace_content(driver)
    logout(driver)

main()
