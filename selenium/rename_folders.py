from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def rename_folders(driver):
    with open('rename_folders.txt', 'r') as rename_list:
        content_line = rename_list.read().splitlines()
        for content in content_line:
            folder_path, new_name = content.split("\t")

            driver.get(my_domain+"/webapps/cmsmain/webui"+folder_path+"?action=details&subaction=bb_directorydetails&uniq=tv2n43&gobackto=dirList-")

            driver.implicitly_wait(3)

            found = False

            try:
                driver.find_element_by_id("newname").clear()
                
                if bool(found) == False:
                    found = True
                    
            except:
                #driver.execute_script("alert('"+old_directory+file+" not found')")
                print(folder_path+" not found")

            if bool(found) == True:

                driver.find_element_by_id("newname").clear()
                driver.find_element_by_id("newname").send_keys(new_name)

                driver.find_element_by_name("bottom_Submit").click()

                driver.implicitly_wait(3)

                try:
                    driver.find_element_by_id("goodMsg1").text
					print("Success: "+folder_path)
					
                except :
                    print("Failed to update: "+folder_path)
                    driver.implicitly_wait(3)

 

def main():
    driver = login()
    rename_folders(driver)
    logout(driver)

main()
