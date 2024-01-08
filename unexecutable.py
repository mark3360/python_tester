#!/bin/python3

import os

filename = os.path.basename(__file__)
lst = filename.split(" - ")
del lst[4:]

(file_id, name, watiam, fileid) = lst



feedback = f"Feedback for {watiam}:\n\n"

feedback += "File Unexecutable!\n"

filename = "../feedback/" + file_id + " - " +  name + " - " +  watiam + " - " +  "feedback.txt"

with open(filename, 'w') as fp:
        fp.write(feedback)
quit()
