from auth import *
import time, re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException

def convert_kaltura_to_item(driver):
    with open('convert_kaltura_to_item.txt', 'r', encoding='utf8') as convert_list:
        content_line = convert_list.read().splitlines()
        for content in content_line:
            course_id, content_id, kaltura_code = content.split("\t")

            driver.get(my_domain+"/webapps/blackboard/execute/manageCourseItem?content_id=_"+content_id+"_1&course_id=_"+course_id+"_1&dispatch=edit")

            try:
                driver.find_element_by_id("htmlData_text").clear()
                driver.execute_script("document.getElementById('htmlData_text').value = '"+kaltura_code.replace("'", "&apos;")+"';")
                driver.find_element_by_name("bottom_Submit").click()

                #try:
                #    WebDriverWait(driver, 3).until(EC.alert_is_present(),
                #                   'Timed out waiting for PA creation ' +
                #                   'confirmation popup to appear.')
                #    alert = driver.switch_to.alert
                #    alert.accept()
    
                #except TimeoutException:
                #    pass

                driver.implicitly_wait(3)

                try:
                    driver.find_element_by_id("goodMsg1").text
                    print("Success: "+course_id+" "+content_id)
                    
                except Exception as e:
                    print("Failed to convert: "+course_id+" "+content_id+" -- "+str(e))
                
            except Exception as e:
                print("Failed to display: "+course_id+" "+content_id+" -- "+str(e))

            


def main():
    driver = login()
    convert_kaltura_to_item(driver)
    logout(driver)

main()
