"""
SÜSSE WURST INSERT SCRIPT CREATOR
AUTHOR: N.F. DESMOND
DATE: JUNE 2025
DESCRIPTION:
This is a basic program for automating the creation of the MySQL insert scripts
for my Süsse Wurst database project. The program first creates three directories:
one for HR insert scripts, one for Store insert scripts, and one for all insert scripts.
Next, it reads CSV files from an HR and Store directory, creating an insert script
for each file and then copying the file twice: once into a schema-specific directory
(HR or Store) and once into a directory storing all of the insert scripts. Finally, 
the program reads each file from the all-inserts directory and combines them into a single
ordered insert script.
"""

import os 
import csv
import shutil
from pathlib import Path


def create_script_directory():
    """Creates three directories for storing insert scripts: one for
       HR inserts, one for Store inserts, and one for all insert scripts.
    """
    directory_name_list = ['sw_hr_inserts', 'sw_store_inserts', 'sw_insert_scripts']
    for dir_name in directory_name_list:
        new_dir = Path(dir_name)
        new_dir.mkdir(exist_ok=True)
    return None


def create_insert_script(csv_file, schema_insert_dir, all_insert_dir, file_prefix):
    """Creates an SQL insert script from a CSV file. One copy is stored in a specific
       schema directory (HR or Store) and another copy is stored in a directory for 
       all insert scripts.
    """
    script_file = f'{file_prefix}_{csv_file.name[0:-4]}_insert.sql' # removes .csv suffix
    table_name = csv_file.name[0:-4]
    with open(csv_file, newline='') as file_read, open(script_file, 'w') as sql_write:
        csv_row_list = []
        csv_reader = csv.reader(file_read)
        sql_write.write(f'INSERT INTO {table_name}\n')
        sql_write.write('VALUES\n')
        for record in csv_reader:
            csv_row_list.append(record)
        for row in csv_row_list:
            sql_write.write('(')
            if row == csv_row_list[-1]:
                row = list(enumerate(row))
                for item in row:
                    if item == row[-1]:
                        item = item[-1]
                        if item.isnumeric() and (len(item) < 5 or len(item) > 5):
                            sql_write.write(f'{item});\n')
                        elif '.' in item:
                            str_item = item.replace('.', '')
                            if str_item.isnumeric():
                                sql_write.write(f'{item});\n')
                            else:
                                sql_write.write(f'"{item}");\n')
                        elif item == 'NULL':
                            sql_write.write(f'{item});\n')
                        else:
                            sql_write.write(f'"{item}");\n')
                    else:
                        item = item[-1]
                        if item.isnumeric() and (len(item) < 5 or len(item) > 5):
                            sql_write.write(f'{item},')
                        elif '.' in item:
                            str_item = item.replace('.', '')
                            if str_item.isnumeric():
                                sql_write.write(f'{item},')
                            else:
                                sql_write.write(f'"{item}",')
                        elif item == 'NULL':
                            sql_write.write(f'{item},')
                        else:
                            sql_write.write(f'"{item}",')
            else:
                row = list(enumerate(row))
                for item in row:
                    if item == row[-1]:
                        item = item[-1]
                        if item.isnumeric() and (len(item) < 5 or len(item) > 5):
                            sql_write.write(f'{item}),\n')
                        elif '.' in item:
                            str_item = item.replace('.', '')
                            if str_item.isnumeric():
                                sql_write.write(f'{item}),\n')
                            else:
                                sql_write.write(f'"{item}"),\n')
                        elif item == 'NULL':
                            sql_write.write(f'{item}),\n')
                        else:
                            sql_write.write(f'"{item}"),\n')
                    else:
                        item = item[-1]
                        if item.isnumeric() and (len(item) < 5 or len(item) > 5):
                                sql_write.write(f'{item},')
                        elif '.' in item:
                                str_item = item.replace('.', '')
                                if str_item.isnumeric():
                                    sql_write.write(f'{item},')
                                else:
                                    sql_write.write(f'"{item}",')
                        elif item == 'NULL':
                            sql_write.write(f'{item},')
                        else:
                            sql_write.write(f'"{item}",')
    shutil.move(script_file, schema_insert_dir)
    shutil.copy(f'{schema_insert_dir}/{script_file}', all_insert_dir)
    
    
def csv_file_to_script(csv_file_dir, schema_insert_dir, all_insert_dir, prefix):
    """Iterates over CSV files in a specified directory and calls the function to create
       insert scripts for each file.
    """
    with os.scandir(csv_file_dir) as file_list:
        for file in file_list:
            create_insert_script(file, schema_insert_dir, all_insert_dir, prefix)

 
def create_ordered_insert(insert_writefile, all_insert_dir):
    """Takes files from the all insert scripts directory and combines them into
       a single ordered insert file.
    """
    with open(insert_writefile, 'a') as file_to_write:
        with os.scandir(all_insert_dir) as insert_list:
            for file in insert_list:
                with open(file, 'r') as file_to_read:
                    line = file_to_read.readline()
                    while line != '':
                        file_to_write.write(line)
                        line = file_to_read.readline()
                    file_to_write.write('\n')
                        
    
if __name__ == '__main__':
    # create directories
    create_script_directory()
    
    # create insert scripts from csv files
    csv_file_to_script('susse_wurst_hr_csv_files', 'sw_hr_inserts', 'sw_insert_scripts', 'hr')
    csv_file_to_script('susse_wurst_store_csv_files', 'sw_store_inserts', 'sw_insert_scripts', 'store')
    
    # create ordered insert file
    create_ordered_insert('sw_database_insert_file.sql', 'sw_insert_scripts')