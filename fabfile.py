from fabric import task, Connection
from terminaltables import DoubleTable
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
def custom_ls(c):
    ls_result = c.local("ls -alh",hide=True)
    ls_output = ls_result.stdout
    split_output = ls_output.split("\n")
    cleaned_lines = list()
    for line in split_output:
        if len(line) != 0:
            cleaned_lines.append(line)
    total_files = len(cleaned_lines) - 1
    table_title = "File Listing ({0} files)".format(total_files)
    table_data = list()
    table_data.append(["Directory / File", "Owner", "Size", "Creation date", "Creation time", "Hidden"])
    for line in cleaned_lines:
        split_line = line.split()
        if len(split_line) > 2:
            directory_file = split_line[-1].strip()
            owner = split_line[3].strip()
            file_size = split_line[4].strip()
            creation_date = split_line[-4].strip() + " " + split_line[-3].strip()
            creation_time = split_line[-2].strip()
            if str(directory_file).startswith("."):
                hidden_status = "True"
            else:
                hidden_status = "False"
            table_data.append([ directory_file, owner, file_size, creation_date, creation_time, hidden_status ])
    double_table = DoubleTable(table_data, table_title)
    print(double_table.table)