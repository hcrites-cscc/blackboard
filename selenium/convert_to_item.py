from auth import *
import time, re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def convert_to_item(driver):
    with open('convert_to_item.txt', 'r') as convert_list:
        content_line = convert_list.read().splitlines()
        for content in content_line:
            course_pk1, content_pk1 = content.split("\t")

            driver.get(my_domain+"/webapps/blackboard/execute/manageCourseItem?content_pk1=_"+content_pk1+"_1&course_pk1=_"+course_pk1+"_1&dispatch=edit")

            try:
                driver.find_element_by_name("bottom_Submit").click()
                driver.implicitly_wait(3)

                try:
                    driver.find_element_by_id("goodMsg1").text
                    print("Success: "+course_pk1+" "+content_pk1)
                    
                except:
                    print("Failed to convert: "+course_pk1+" "+content_pk1)
                
            except:
                print("Failed to display: "+course_pk1+" "+content_pk1)

            


def main():
    driver = login()
    convert_to_item(driver)
    logout(driver)

main()
