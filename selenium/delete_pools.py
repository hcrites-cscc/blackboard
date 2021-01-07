from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def delete_pools(driver):
    with open('delete_pools.txt', 'r') as delete_list:
        content_line = delete_list.read().splitlines()
        for content in content_line:
            course_pk1, pool_pk1, pool_title = content.split("\t")
            
            driver.get(my_domain+"/webapps/assessment/do/authoring/viewAssessmentManager?assessmentType=Pool&course_id=_"+course_pk1+"_1")

            driver.execute_script("document.getElementsByName('assessmentId')[0].value='"+pool_pk1+"'")
            driver.execute_script("document.getElementsByName('method')[0].value='removeAssessment'")
            driver.execute_script("document.getElementById('assessmentManagerForm').submit()")
            
            driver.implicitly_wait(3)

            try:
                driver.find_element_by_id("goodMsg1").text
				print("Success: "+pool_pk1+" "+pool_title)
				
            except:
                print("Failed to delete: "+pool_pk1+" "+pool_title)

def main():
    driver = login()
    delete_pools(driver)
    logout(driver)

main()
