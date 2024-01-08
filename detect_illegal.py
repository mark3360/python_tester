#!/bin/python3

import os
import re

directory = "testing_directory/"

def sanitize(file):
    file = open(file, "r")
    text = file.read()
    res = re.findall('\sos[\s|"]', text)
    res += re.findall('\ssys[\s|"]', text)
    return res


for filename in os.listdir(directory):
    lst = filename.split(" - ")
    del lst[4:]
    (file_id, Name, watiam, file) = lst
    path = directory + filename
    illegal_phrases = sanitize(path)
    
    if illegal_phrases != []:
        print(f"Testing of student {name} aborted due to illegal phrase(s)")
        print(illegal_phrases)


