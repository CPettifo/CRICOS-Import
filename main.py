# The goal of this script is to allow for the analysis of structured HEI data to allow for insertion into the 
# World Higher Education Database, the first iteration uses CRICOS but given time I plan to modify this to take
# any structured data as input


import categorise # type: ignore

masterlist_path = "masterlist.xlsx"
glossary_path = "glossary.xlsx"


# Ask for user input if categorisation is required
# user_input = input("categorise institutions? [Y/ N]: ")

user_input = "Y"

if user_input == "Y":
    
    # list of level codes that categorise a degree as postgrad in the WHED
    postgrad_codes = ["6C", "7A", "7B", "7C", "7D"]
    
    # Categorise institutions (WHED-Recognised, WHED-Candidate, etc.)
    categorise.main(glossary_path, masterlist_path, postgrad_codes)


print("Continuing")