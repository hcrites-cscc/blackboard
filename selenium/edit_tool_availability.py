from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def edit_tool_availability(driver):
    with open('edit_tool_availability.txt', 'r') as edit_list:
        content_line = edit_list.read().splitlines()
        for content in content_line:
            course_pk1, tools = content.split("\t")
            list_of_tools = tools.split("|")

            driver.get(my_domain+"/webapps/blackboard/execute/course/tools/settings?dispatch=viewToolsSettings&course_id=_"+course_pk1+"_1")

            driver.implicitly_wait(3)

            found = False         
	
            for tool in list_of_tools:
                try:
                    driver.execute_script("checkbox = document.getElementById('available__"+tool+"_1'); if(checkbox.checked) {checkbox.click();}")
                    driver.implicitly_wait(20)
                    #driver.find_element_by_name("available__"+tool+"_1").click()
                    
                    if bool(found) == False:
                        found = True
                        
                except:
                    #driver.execute_script("alert('"+old_directory+file+" not found')")
                    print(course_pk1+tool+" not found")
            
            if bool(found) == True:
                driver.find_element_by_id("bottom_Submit").click()
                driver.implicitly_wait(3)

                try:
                    print(driver.find_element_by_id("goodMsg1").text)
					print("Success: "+course_pk1)
					
                except:
                    print("element not found")

def main():
    driver = login()
    edit_tool_availability(driver)
    logout(driver)

main()
