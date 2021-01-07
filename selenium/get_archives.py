from auth import *
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def get_archives(driver):
    with open('get_archives.txt', 'r') as archive_list:
        course_line = archive_list.read().splitlines()

        timestamp = datetime.now()
        timestamp_string = str(timestamp.year)+str(timestamp.month)+str(timestamp.day)+str(timestamp.hour)+str(timestamp.minute)+str(timestamp.second)

        archive_file = open("archives-"+timestamp_string+".htm", "a+")
        archive_file.write("<html><head><title>Archives</title></head><body>")
        
        for course in course_line:
            
            driver.get(my_domain+"/webapps/blackboard/admin/archive_manager.jsp?navItem=cp_course_utilities_export&course_id=_"+course+"_1&contextNavItem=control_panel")
            driver.implicitly_wait(3)

            links = driver.find_elements_by_css_selector("table#listContainer_datatable a")

            for link in links:
                link_href = link.get_attribute("href")
                link_name = link.get_attribute("innerHTML")

                if link_name.find("ArchiveFile_") != -1:
                    link_contents = "<a href='"+link_href+"'>"+link_name+"</a><br />"
                    archive_file.write(link_contents)
                    print(link_name)
                    exit
                    

        archive_file.close()

def main():
    driver = login()
    get_archives(driver)
    logout(driver)

main()
