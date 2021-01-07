from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def copy_files(driver):
    with open('copy_files.txt', 'r') as copy_list:
        content_line = copy_list.read().splitlines()
        for content in content_line:
            new_directory, old_directory, files = content.split("\t")
            list_of_files = files.split("|")

            driver.get(my_domain+"/webapps/cmsmain/webui"+old_directory+"?sortDir=ASCENDING&subaction=view&action=frameset&uniq=tv2n43&editPaging=true&numResults=1000&startIndex=1000")

            driver.implicitly_wait(3)

            found = False         
	
            if list_of_files[0] == "AllFiles":
                try:
                    driver.find_element_by_id("listContainer_selectAll").click()
                    if bool(found) == False:
                        found = True
                    
                except NoSuchElementException:
                    print("'Click All' not found")  
                    
            else:
                for file in list_of_files:
                    try:
                        driver.find_element_by_xpath("//input[@value='"+old_directory+file+"']").click()
                        #print(old_directory+file+" found")
                        if bool(found) == False:
                            found = True
                            
                    except:
                        #driver.execute_script("alert('"+old_directory+file+" not found')")
                        print(old_directory+file+" not found")
            
            if bool(found) == True:
                driver.execute_script("csfunctions.copyFiles('Recycle Bin')")
                driver.implicitly_wait(3)
                driver.find_element_by_id("targetPath_CSFile").send_keys(new_directory)
                driver.find_element_by_id("bottom_Submit").click()
                driver.implicitly_wait(3)

                try:
                    print(driver.find_element_by_id("goodMsg1").text)
                except:
                    print("element not found")

def main():
    driver = login()
    copy_files(driver)
    logout(driver)

main()
