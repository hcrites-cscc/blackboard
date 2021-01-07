from auth import *
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def delete_files(driver):
    with open('delete_course_home_directory.txt', 'r') as delete_file:
        delete_list = delete_file.read().splitlines()
        for course_id in delete_list:
            driver.get(my_domain+"/webapps/cmsmain/webui"+course_id+"?sortDir=ASCENDING&subaction=view&action=frameset&uniq=tv2n43&editPaging=true&numResults=1000&startIndex=1000")
            driver.implicitly_wait(3)

            document_body = driver.find_element_by_id("containerdiv").text

            if document_body.find("Cannot display that location.") >= 0 or document_body.find("specified resource was not found") >= 0:
                print(course_id+" not found")

            else:
                files_count = driver.find_element_by_id("numFiles").get_property("value")
                files_form = driver.find_element_by_name("filesForm").text
                
                if files_form.find("Folder Empty") >= 0:
                    print(course_id+" empty")

                else:
                    subaction = driver.find_element_by_id("subaction").get_property("value")

                    if subaction=="deleteforce":
                        print(course_id+" done")
                        
                    else:
                        driver.find_element_by_id("listContainer_selectAll").click()
                        xid_count = 0

                        if files_form.find("xid-") >= 0:
                            file_inputs = driver.find_elements_by_tag_name("input")
                            for field in file_inputs:
                                if field.get_attribute("type") == "checkbox":
                                    if field.text.find("xid-") >= 0:
                                        ++xid_count
                                        field.click()
                        if xid_count == files_count:
                            print(course_id+" only xid files")
                        else:
                            driver.execute_script("var selectedFiles = csfunctions.getSelectedFiles();FileFolderRemoval.getNumberOfFilesWithLinks( selectedFiles, function(numFiles) {if (numFiles > 0 && selectedFiles.length >= 1){document.filesForm.a1.value = 'multiple';document.filesForm.subaction.value = 'listfileswithlinks';document.filesForm.action = csfunctions.origAction;document.filesForm.submit();return;}document.filesForm.a1.value = 'multiple';document.filesForm.subaction.value = 'deleteforce';document.filesForm.action = csfunctions.origAction;document.filesForm.submit();});")
                            driver.implicitly_wait(5)
                            


def main():
    driver = login()
    delete_files(driver)
    logout(driver)

main()
