from selenium import webdriver
import csv

'''
    Simple crawl data 2: get missing data from data-all-html.csv
'''


def get_html(html_file_name):
    with open(html_file_name, 'r') as csv_file:
        rf = csv.reader(csv_file)
        school_all = list(rf)

    school_name_url = {}

    for iSchool in school_all:
        curr_school = iSchool[0]

        id_school_id = curr_school.index('clblue2">', 0)
        id_end_school_id = curr_school.index('<', id_school_id+len('clblue2">'))
        school_id = curr_school[id_school_id+len('clblue2">'):id_end_school_id]

        id_title = curr_school.index('title="', 0)
        id_end_title = curr_school.index('"', id_title+len('title="'))
        title_school = curr_school[id_title+len('title="'):id_end_title]

        id_url = curr_school.index('href="', 0)
        id_end_url = curr_school.index('"', id_url+len('href="'))
        url_school = curr_school[id_url+len('href="'):id_end_url]

        school_name_url[school_id] = [title_school, url_school]

    return school_name_url


def main():
    school_all = get_html('data-all-html.csv')

    school_all_it = {}
    driver = webdriver.Chrome()
    count = 0
    for title in school_all:
        count += 1
        # page = urllib.request.urlopen(school_all[title])
        print(school_all[title][0])
        driver.get(school_all[title][1])
        driver.implicitly_wait(10)

        text_list = ["Công nghệ thông tin", "748", "Truyền thông đa phương tiện", "7320104", "Thương mại điện tử", "7340122", "Hệ thống thông tin quản lý",
                     "7340405", "Toán tin", "7460117", "Khoa học máy tính", "Mạng máy tính và truyền thông dữ liệu", "Kỹ thuật phần mềm", "Hệ thống thông tin", "Kỹ thuật máy tính",
                     "Công nghệ kỹ thuật máy tính", "An toàn thông tin"]

        for i_text in text_list:
            a = driver.find_element_by_tag_name("body").text
            is_it = a.find(i_text)
            if is_it != -1:
                school_all_it[title] = [school_all[title][0], school_all[title][1], 'yes']
                break

    with open('data_new.csv', 'w') as csv_file:
        wr = csv.writer(csv_file)
        for key, value in school_all_it.items():
            wr.writerow([key, value[0], value[1]])


def merge_data():
    with open('data_new.csv', 'r') as csv_file:
        rd = csv.reader(csv_file)
        school_it_new = {rows[0]: rows[1:3] for rows in rd}

    with open('data_all_old.csv', 'r') as csv_file:
        rd = csv.reader(csv_file)
        school_it_old = {rows[0]:rows[1] for rows in rd}

    school_it_merge = school_it_new
    for key, value in school_it_old.items():
        if school_it_merge.get(key) is None:
            school_it_merge[key] = value
        else:
            print(key + ' existed')

    with open('data_merge.csv', 'w') as csv_file:
        wr = csv.writer(csv_file)
        for key, value in school_it_merge.items():
            if type(value) == list:
                wr.writerow([key, value[0], value[1]])
            else:
                wr.writerow([key, value])


merge_data()
