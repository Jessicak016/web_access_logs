# -*- coding: utf-8 -*-
#!/usr/bin/python -tt
import re
import csv
from collections import defaultdict


def write_log_entries(filename, list_of_rows_to_write):
    row_counter = 0
    with open(filename, 'w+', newline = '') as f:
        row_writer = csv.DictWriter(f, delimiter='\t', quotechar='"', extrasaction='ignore',
                                    fieldnames=["IP", "Ignore1", "Ignore2", "Timestamp", "Ignore3", "HTTP_Verb",
                                                "HTTP_Status", "HTTP_Duration", "HTTP_Redirect", "Browser_Type",
                                                "Top_Level_Domain"])
        row_writer.writeheader()
        for row in list_of_rows_to_write:
            row_writer.writerow(row)
            row_counter = row_counter + 1

    print("Wrote {} rows to {}".format(row_counter, filename))

# Function get_top-level_domain:
#    Input:  A string containing a URL
#    Output:  the top-level domain in the URL, or None if no valid top-level domain was found.  The top-level
#             domain, if it exists, should be normalized to always be in lower case.




def get_toplevel_domain(url):
    match = re.search(r"(?<=[a-zA-Z]\.)([a-zA-Z]{2,3})(?=\/|\:)", url)
    if match == None:
        return (url, None)
    return (url, match.group(1).lower())

# Function read_log_file:
#   Input: the file name of the log file to process
#   Output:  A two-element tuple with element 0 a list of valid rows, and element 1 a list of invalid rows
def read_log_file(filename):
    valid_entries   = [] #create an empty list to be put into tuple
    invalid_entries = [] #create an empty list to be put into tuple

    with open(filename, 'r', newline='') as input_file:
        log_data_reader = csv.DictReader(input_file, delimiter='\t', quotechar ='"', skipinitialspace=True,
                                         fieldnames=["IP","Ignore1","Ignore2","Timestamp","Ignore3","HTTP_Verb","HTTP_Status","HTTP_Duration","HTTP_Redirect","Browser_Type"])
        for row in log_data_reader:
            not_a_valid_line = False
            url = row['HTTP_Verb']
            statuscode = row['HTTP_Status']
            getposthttp_match = re.search(r"^(GET|POST)\shttps?://[a-zA-Z]+.+(?=\/|HTTP\/\s1\.\d)", url)
            if getposthttp_match == None:
                not_a_valid_line = True
            else:
                if statuscode == "200":
                    toplevel_domain = get_toplevel_domain(getposthttp_match.group())
                    if toplevel_domain:
                        not_a_valid_line = False
                    else:
                        not_a_valid_line = True
                else:
                    not_a_valid_line = True



            if not_a_valid_line:
                invalid_entries.append(row)
                continue

            valid_entries.append(row)


    return (valid_entries, invalid_entries)

def main():
    valid_rows, invalid_rows = read_log_file(r'access_log.txt') #output of read_log_file is a tuple of lists

    write_log_entries('valid_access_log_jessjkim.txt', valid_rows)
    write_log_entries('invalid_access_log_jessjkim.txt', invalid_rows)

# This is boilerplate python code: it tells the interpreter to execute main() only
# if this module is being run as the main script by the interpreter, and
# not being imported as a module.
if __name__ == '__main__':
    main()
