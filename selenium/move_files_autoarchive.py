from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def move_files_autoarchive(driver):
    with open('move_files_autoarchive.txt', encoding='utf8', mode='r') as move_list:
        content_line = move_list.read().splitlines()
        for content in content_line:
            archive_folder, new_directory = content.split("\t")

            driver.get(my_domain+"/webapps/cmsmain/webui/internal/autoArchive?sortDir=ASCENDING&subaction=view&action=frameset&uniq=-quealr&editPaging=true&numResults=1")

            driver.implicitly_wait(3)

            driver.find_element_by_name("file0").click()
            driver.execute_script("csfunctions.moveFiles('Recycle Bin')")

            driver.implicitly_wait(3)
            driver.execute_script("document.getElementById('file0').value = '"+archive_folder+"';")
            driver.find_element_by_id("targetPath_CSFile").send_keys(new_directory)
            driver.find_element_by_id("bottom_Submit").click()
            driver.implicitly_wait(3)

            try:
                driver.find_element_by_id("goodMsg1").text
                print("Success: "+archive_folder)
            except:
                print("Failed to move: "+archive_folder)

                

def main():
    driver = login()
    move_files_autoarchive(driver)
    logout(driver)

main()
