from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def create_folders(driver):
    with open('create_folder_content_collection.txt', encoding='utf8', mode='r') as folder_list:
        folder_line = folder_list.read().splitlines()
        for folder in folder_line:
            parent_directory, new_directory = folder.split("\t")

            driver.get(my_domain+"/webapps/cmsmain/webui"+parent_directory+"?sortDir=ASCENDING&subaction=view&action=frameset&uniq=tv2n43&editPaging=true&numResults=10&startIndex=0")

            driver.implicitly_wait(3)

            driver.find_element_by_id("newAddFolderButton").click()
            driver.find_element_by_id("newFolderName").send_keys(new_directory)
            driver.find_element_by_id("addFolderFormSubmit").click()
                     
            driver.implicitly_wait(3)

            try:
                driver.find_element_by_id("goodMsg1").text
				print("Success: "+parent_directory+"/"+new_directory)
				
            except:
                print("Failed to create: "+parent_directory+"/"+new_directory)

def main():
    driver = login()
    create_folders(driver)
    logout(driver)

main()
