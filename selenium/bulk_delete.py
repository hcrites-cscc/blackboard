from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def bulk_delete(driver):
    with open('bulk_delete.txt', 'r') as delete_list:
        course_line = delete_list.read().splitlines()
        for course in course_line:
            
            driver.get(my_domain+"/webapps/blackboard/execute/recycler?course_id=_"+course+"_1&action=select&context=COURSE")
            driver.implicitly_wait(3)

            driver.execute_script("var d=window.frames[0]?content.document:document;for(var x=0;x<d.forms.length;x++){var cSet=d.forms[x].elements;for(var i=0; i<cSet.length;i++){if(cSet[i].type=='checkbox'){cSet[i].checked=cSet[i].checked?false:true;cSet[i].disabled=false;}if(cSet[i].value=='statistics'||cSet[i].value=='users'||cSet[i].value=='STATISTICS'||cSet[i].value=='USERS'){cSet[i].checked=false;}}}")
            driver.implicitly_wait(3)
            
            driver.find_element_by_id("confirmation").send_keys("Delete")

            driver.find_element_by_id("bottom_Submit").click()
            driver.implicitly_wait(5)

            try:
                driver.find_element_by_id("goodMsg1").text
                print("Success: "+course)
            except:
                print("Failure: "+course)

def main():
    driver = login()
    bulk_delete(driver)
    logout(driver)

main()
