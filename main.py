# The goal of this script is to allow for the analysis of structured HEI data to allow for insertion into the 
# World Higher Education Database, the first iteration uses CRICOS but given time I plan to modify this to take
# any structured data as input
#TODO put this into the README too (or instead of)
# The structured data is outlined in the README but I've put it here for myself also

# there should be three spreadsheets in your workbook
# ext_inst is a list of the institutions from the recognised government or credential recognition body
# It should have the following columns in this order: row index, institution ID, institution name, institution alternative name, institution homepage,
# a concatenation of the institutional address
# 
# ext_cred is a list of the credentials offered 
# It should have the following columns in this order: institution ID, institution name, whether credential is not expired (manually set this to "No" if it is not present in extraction)
# Credential level (i.e. Bachelors, Masters, or NQF level), Course Name, Course Code, FOS Levels if available and in descending order of hierarchy

# I'm not planning for this to be particularly well optimised, as it is a script that will only be run periodically, and likely on local systems in the background.

import categorise, creds #type ignore


masterlist_path = "masterlist.xlsx"
output_path = "output.xlsx"

# Ask for user input if categorisation is required
user_input = input("categorise institutions? [Y/ N]: ")


if user_input == "Y":
    
    # list of level codes that categorise a degree as postgrad in the WHED
    postgrad_codes = ["6C", "7A", "7B", "7C", "7D"]

    # Categorise institutions (WHED-Recognised, WHED-Candidate, etc.) and export to an excel spreadsheet
    categorise.main(masterlist_path, postgrad_codes)

user_input = input("do you want to attempt to insert into the whed using masterlist credentials?")
if user_input == "Y":
    creds.main(masterlist_path, output_path, insts)    
    exit(0)