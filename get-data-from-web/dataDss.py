from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import csv

'''
    Simple crawl data: get information about university has IT-related major
'''


def main():
    url = "https://thituyensinh.vn/frontendTs/faces/TraCuu?_adf.ctrl-state=oyuu9sijz_14&_afrLoop=11607479606302706l"
    dataDss = []
    noDataSchool = []

    # create a new Chrome session
    driver = webdriver.Chrome()

    driver.get(url)
    driver.implicitly_wait(10)

    pages = Select(driver.find_element_by_id('pt1:r1:0:sf1:soc3::content'))
    pages.select_by_value('8')

    # run this 4 times for easier debug when error
    for elementId in range(301, 440):
        idStr = 'pt1:r1:0:sf1:t2:' + str(elementId) + ':j_id__ctru52pc2'
        element = driver.find_element_by_id(idStr)
        elementText = element.text
        if ("trung cấp" not in elementText) and ("Trung cấp" not in elementText) and ("Trung Cấp" not in elementText) and ("Cao đẳng" not in elementText) and ("Cao Đẳng" not in elementText):
            element.click()

            try:
                schoolId = driver.find_element_by_id('pt1:r1:0:ot2').text
                resultITSchool = driver.find_elements_by_xpath("//*[contains(text(), '748')]")
                if len(resultITSchool) != 0:
                    addressSchool = driver.find_element_by_id('pt1:r1:0:ot3').text
                    phoneSchool = driver.find_element_by_id('pt1:r1:0:ot9').text
                    websiteSchool = driver.find_element_by_id('pt1:r1:0:gl1').text
                    dataDss.append([schoolId, elementText, addressSchool, phoneSchool, websiteSchool])

            except NoSuchElementException:
                noDataSchool.append([elementText])
                # print(elementText)

            finally:
                driver.back()
                pages = Select(driver.find_element_by_id('pt1:r1:0:sf1:soc3::content'))
                pages.select_by_value('8')


    # driver.close()

    with open('dataSchoolIT4.csv', 'w') as csvFile:
        wr = csv.writer(csvFile)
        wr.writerows(dataDss)

    with open('noDataSchool4.csv', 'w') as csvFile:
        wr = csv.writer(csvFile)
        wr.writerows(noDataSchool)
