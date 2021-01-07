from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def delete_files(driver):
    with open('delete_files.txt', 'r') as delete_list:
        content_line = delete_list.read().splitlines()
        for content in content_line:
            directory, files = content.split("\t")
            list_of_files = files.split("|")

            driver.get(my_domain+"/webapps/cmsmain/webui"+directory+"?sortDir=ASCENDING&subaction=view&action=frameset&uniq=tv2n43&editPaging=true&numResults=1000&startIndex=1000")

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
                        driver.find_element_by_xpath("//input[@value='"+directory+file+"']").click()
                        #print(old_directory+file+" found")
                        if bool(found) == False:
                            found = True
                            
                    except:
                        #driver.execute_script("alert('"+old_directory+file+" not found')")
                        print(directory+file+" not found")
            
            if bool(found) == True:
                driver.execute_script("csfunctions.deleteFilesFolders();")

                confirmation = driver.switch_to.alert
                confirmation.accept()
                                
                driver.implicitly_wait(3)

                try:
                    print(driver.find_element_by_id("goodMsg1").text)
					print("Success: "+directory)
					
                except:
                    print("element not found")

def main():
    driver = login()
    delete_files(driver)
    logout(driver)

main()
