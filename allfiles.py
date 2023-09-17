# allfiles.py (2023-09-17)
# Copyright (c) 2023 Mikko Mononen
# MIT License

import os
import zipfile
from datetime import datetime
from textwrap import wrap

# diz-file encoding setting try 'utf-8' or 'ascii'
ENC = 'ascii' 
CODEPAGE = 'cp858'
LINE_LENGTH = 72 # max line length in results
OUTPUT_FILE = '00FILES.TXT'
DIZ_FILE = 'file_id.diz'

result_file = []
num_zips = 0 # number of zips
num_dizes = 0 # number of zips with dizes

dir_contents = os.listdir()

# Go through all files in dir
for filename in dir_contents:
    # get file stats (for file size)
    file_stats = os.stat(filename)
    # Split filenames by dots
    split_this = filename
    splitted_list = split_this.split('.')
    # The last part should be the file extension
    # Check if file extension is zip
    if splitted_list[len(splitted_list) - 1] == 'zip' or splitted_list[len(splitted_list) - 1] == 'ZIP':                
        # try to read file_id.diz in zip file
        num_zips += 1
        diz_content = ""
        diz_lines = ""
        # print(f"Reading: {filename}")
        try:
            # zip handler
            zip = zipfile.ZipFile(filename)
            # open file_id.diz
            f = zip.open(DIZ_FILE)
            # read contents of file_id.diz
            diz_content = f.read()
            # close file_id.diz file
            f.close()
            if len(diz_content) > 0:
                # decode binary diz_content to string
                diz_lines = diz_content.decode(ENC)
                # replace new lines with spaces
                diz_lines = " ".join(diz_lines.splitlines())
                # get file_id.diz's date
                dt = f"{zip.getinfo(DIZ_FILE).date_time[0]}-{zip.getinfo('file_id.diz').date_time[1]}-{zip.getinfo('file_id.diz').date_time[2]}"
                # get file size
                filesize = file_stats.st_size
                # For larger files use either kB or MB depending on size
                if filesize >= (1024*1024):
                    filesize_text = f"{file_stats.st_size / (1024 * 1024):.2f} MB"
                elif filesize < 1024:
                    filesize_text = f"{file_stats.st_size} bytes"
                else:
                    filesize_text = f"{file_stats.st_size / 1024:.2f} kB"
                result_file.append(f"{filename} [{dt}] [{filesize_text}]")
                # wrap diz lines to line length
                diz_lines = wrap(diz_lines, LINE_LENGTH)
                # four spaces indentation for diz descriptions
                for line in diz_lines:
                    result_file.append(f"    {line}")
                num_dizes += 1
        except:
            # print(f"Bad zip file or no file_id.diz: {filename}")
            pass
print(f"{len(dir_contents)} files found.")
print(f"Found {num_zips} zip archives with {num_dizes} {DIZ_FILE} files in them.")
with open(OUTPUT_FILE, "w", encoding=CODEPAGE) as txt_file:
    for line in result_file:
        txt_file.write("".join(line) + "\n")
print(f"Results written in '{OUTPUT_FILE}'.")