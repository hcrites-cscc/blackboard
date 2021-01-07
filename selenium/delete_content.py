from auth import *
import time, re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException

def delete_content(driver):
    with open('delete_content.txt', 'r') as copy_list:
        content_line = copy_list.read().splitlines()
        for content in content_line:
            course_id, parent_id, content_id = content.split("\t")    

            driver.get(my_domain+"/webapps/blackboard/content/listContentEditable.jsp?content_id=_"+parent_id+"_1&course_id=_"+course_id+"_1")
            drop_down = driver.find_element_by_xpath("//div[@id='_"+content_id+"_1']/span/a")

            delete_id = drop_down.get_attribute("id").replace("cmlink_","")

            drop_down.click()

            driver.implicitly_wait(1)

            driver.find_element_by_id("remove_"+delete_id).click()

            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present(),
                               'Timed out waiting for PA creation ' +
                               'confirmation popup to appear.')
                alert = driver.switch_to.alert
                alert.accept()

            except TimeoutException:
                pass
            
            driver.implicitly_wait(3)

            try:
                driver.find_element_by_id("goodMsg1").text
                print("Success: "+course_id+" "+content_id)
            except :
                print("Failed to update: "+course_id+" "+content_id)
                driver.implicitly_wait(3)


def main():
    driver = login()
    delete_content(driver)
    logout(driver)

main()
