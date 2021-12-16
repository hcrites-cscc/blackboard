from auth import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


def add_collaborate_menu_item(driver):
    with open('add_collaborate_menu_item.txt', 'r', encoding='utf8') as course_file:
        course_lines = course_file.read().splitlines()
        for course_id in course_lines:

            driver.get(my_domain+"/webapps/blackboard/admin/archive_manager.jsp?navItem=cp_course_utilities_export&course_id=_"+course_id+"_1&contextNavItem=control_panel")

            try:
                # Ensure Edit Mode is enabled
                editmode_status = driver.find_element_by_id("statusText").text

                if editmode_status.find("OFF") != -1:
                    driver.find_element_by_id("editModeToggleLink").click()
                    driver.implicitly_wait(3)

                # Click the Add Menu Item +
                driver.find_element_by_id("addCmItem").click()

                # Click Tool Link
                driver.find_element_by_id("addToolLinkButton").click()

                # Enter Name
                driver.find_element_by_id("addToolLinkName").send_keys("Collaborate")

                # Select Blackboard Collaborate Ultra
                driver.find_element_by_id("toolSelect").click()
                tool_select = Select(driver.find_element_by_id("toolSelect"))
                tool_select.select_by_value("bb-collab-ultra")

                # Make visible to students
                driver.find_element_by_xpath("//input[@id='tool_link_availability_ckbox']").click()

                # Submit the Form
                driver.find_element_by_id("addToolLinkFormSubmit").click()

                driver.implicitly_wait(3)
                print("Created: "+course_id)

                
            except Exception as e:
                print("Failed to display: "+course_id+" -- "+str(e))

            


def main():
    driver = login()
    add_collaborate_menu_item(driver)
    logout(driver)

main()
