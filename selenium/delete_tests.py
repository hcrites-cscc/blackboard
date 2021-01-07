from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def delete_tests(driver):
    with open('delete_tests.txt', 'r') as delete_list:
        content_line = delete_list.read().splitlines()
        for content in content_line:
            course_pk1, test_pk1, test_title = content.split("\t")

            driver.get(my_domain+"/webapps/assessment/do/authoring/viewAssessmentManager?assessmentType=Test&course_id=_"+course_pk1+"_1")

            driver.execute_script("document.getElementsByName('assessmentId')[0].value='"+test_pk1+"'")
            driver.execute_script("document.getElementsByName('method')[0].value='removeAssessment'")
            driver.execute_script("document.getElementById('assessmentManagerForm').submit()")
            
            driver.implicitly_wait(3)

            try:
                driver.find_element_by_id("goodMsg1").text
                print("Success: "+test_pk1+" "+test_title)
                
            except:
                print("Failed to delete: "+test_pk1+" "+test_title)

def main():
    driver = login()
    delete_tests(driver)
    logout(driver)

main()
