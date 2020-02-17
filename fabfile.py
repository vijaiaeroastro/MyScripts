from fabric import task, Connection
from terminaltables import DoubleTable, SingleTable
import os

@task
def append_path_in_bash(c):
    current_working_directory = os.getcwd()
    home_directory = os.path.expanduser("~") + "/"
    bashrc_file = open("{0}/.bashrc".format(home_directory), 'a+')
    bashrc_file.write("export PATH={0}:$PATH\n".format(current_working_directory))
    bashrc_file.close()
    c.local("source ~/.bashrc")

@task 
def custom_ls(c, show_hidden_files=''):
    contains_symlinks = False
    ls_result = c.local("ls -alh",hide=True)
    ls_output = ls_result.stdout
    split_output = ls_output.split("\n")
    cleaned_lines = list()
    for line in split_output:
        if len(line) != 0:
            cleaned_lines.append(line)
    for line in cleaned_lines:
        if "->" in line:
            contains_symlinks = True
    table_data = list()
    if show_hidden_files == 'True':
        if contains_symlinks:
            table_data.append(["Directory / File", "Symlink", "Owner", "Size", "Creation date", "Creation time", "Hidden"])
        else:    
            table_data.append(["Directory / File", "Owner", "Size", "Creation date", "Creation time", "Hidden"])
    else:
        if contains_symlinks:
            table_data.append(["Directory / File", "Symlink", "Owner", "Size", "Creation date", "Creation time"])
        else:    
            table_data.append(["Directory / File", "Owner", "Size", "Creation date", "Creation time"])
    for line in cleaned_lines:
        split_line = line.split()  
        if len(split_line) > 2:
            directory_file = ""
            symlink = ""
            owner = ""
            file_size = ""
            creation_date = ""
            creation_time = ""
            if not split_line[-2].strip() == "->":
                directory_file = split_line[-1].strip()
            else:
                directory_file = split_line[-1]
                symlink = split_line[-3].strip()
            owner = split_line[3].strip()
            file_size = split_line[4].strip()
            creation_date = split_line[5].strip() + " " + split_line[6].strip()
            creation_time = split_line[7].strip()
            if not show_hidden_files == 'True':
                if str(directory_file).startswith("."):
                    continue
            if show_hidden_files == 'True':
                hidden_status = ''
                if str(directory_file).startswith("."):
                    hidden_status = 'True'
                else:
                    hidden_status = 'False'
                if contains_symlinks:    
                    table_data.append([ directory_file, symlink, owner, file_size, creation_date, creation_time, hidden_status ])
                else:    
                    table_data.append([ directory_file, owner, file_size, creation_date, creation_time, hidden_status ])
            else:
                if contains_symlinks:           
                    table_data.append([ directory_file, symlink, owner, file_size, creation_date, creation_time ])
                else:
                    table_data.append([ directory_file, owner, file_size, creation_date, creation_time ])   
    total_files = len(table_data) - 1
    table_title = "File Listing ({0} files)".format(total_files)
    double_table = SingleTable(table_data, table_title)
    double_table.inner_row_border = True
    print(double_table.table)