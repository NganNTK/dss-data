import pandas as pd
import os

with open('data_final_160_schools.csv', 'r') as csv_file:
    data_school = pd.read_csv(csv_file)

folder_path = 'data_final_160_schools/'


def data_2_sql_table():
    data_header = data_school.columns.values
    print(data_header)

    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)

    # table_cols: {table name - [cols put in table, primary key]}
    table_cols = {'r1-schools': [["MaTruong", "TenTruong", "DiaChi", "Website", "TinhThanh", "DVChuQuan"], 'MaTruong'],
                  'r2-majors': [["MaTruong", "MaNganh", "DiemChuan", "ChiTieu"], 'MaNganh'],
                  'r3-schools-majors': [["MaTruong", "MaNganh", "DiemChuan", "ChiTieu"], ['MaTruong', 'MaNganh']]}

    for table_name, cols in table_cols.items():
        split_data(table_name, cols)


def split_data(table_name, cols):
    r = data_school[cols[0]]
    r = r.drop_duplicates(subset=cols[1], keep='last')

    with open(folder_path + table_name + '.csv', 'w') as csv_file:
        r.to_csv(csv_file, index=False)


def list_data_new():
    with open('data_merge.csv', 'r') as csv_file:
        data_school_new = pd.read_csv(csv_file, header=None)

    id_school_old = data_school[["Mã"]]
    id_school_new = data_school_new[0]

    for school in id_school_new:
        if not (school in id_school_old.values):
            print(school)


data_2_sql_table()
