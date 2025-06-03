from openpyxl import load_workbook #type: ignore
import os

# CRICOS is an Australian Credential Registry that does not have an API, they do however regularly export from their database and release exports to the public as excel spreadsheets.
# The World Higher Education Database (WHED) aims to catalogue every higher education institution in the world including institutional and credential information.

# The purpose of this script is to process the data within the CRICOS exports and import it directly into the WHED to semi-automate the update process for Australia.


# Before the process begins the latest list of WHED-recognised institutions in Australia is exported with their ID and added as a sheet in the masterlist

# The main method is called by the main.py script
def main(glossary_path):
    ###Initialise Variables###
    # WHED-Recognised Institutions not recognised by CRICOS
    whed_check = 0

    # WHED-Candidates within CRICOS
    whed_candidates = 0

    # Non WHED-Level Institutions
    whed_excluded = 0

    if not os.path.exists(glossary_path):
        print(f"Masterlist not found {glossary_path}")
        return

    # Read masterlist
    print(f"Opening glossary: {glossary_path}")
    wb = load_workbook(glossary_path)

    # open the whed_levels sheet
    whed_levels = wb['whed_levels']

    ###Initialise Lists###

    # List of Level Codes that are considered post-grad by the WHED
    postgrad_codes = ["6C", "7A", "7B", "7C", "7D"]

    # List of credential titles from the spreadsheet (this could later be turned into a query by )
    print("Checking postgrad degrees")
    postgrad_list = get_postgrad_list(postgrad_codes, whed_levels)

    print(f"List of postgrad credentials offered in this country:\n{postgrad_list}")


    # For each institution
        # Check that they are considered by CRICOS as Active

        #TODO Create a function that will take as input an institution name, list of credentials for each category

        # Offers >= Bachelor Honours, these are WHED candidates (will have to check whether they have a certain number of graduate cohorts)


        # Else whed_excluded

        #TODO Create function that takes as input the institution name
        # Same as above but name matches WHED-Recognised institutions

        # Add column for excluded categories, 
        # in CRICOS but not WHED-level (i.e. doesn't offer Honours+)
        # Not in CRICOS or name mismatch

    # Save output
    wb.save("output.xlsx")

#TODO Flesh out this function
# Checks the credentials offered at a specific institution to see if it is a possible WHED candidate
def whed_check():
    return 0


# Prints a summary of the categorisation process in the terminal
def output_summary():
    return 0


# Takes the list of postgrad codes and the whed_levels sheet as input and returns a list of course names at post-grad level
def get_postgrad_list(postgrad_codes, whed_levels):
    postgrad_list = []
    
    # for row of credential name
    for row in whed_levels.iter_rows(min_row=2, values_only = True):
        cred_name = str(row[0])
        level_code= str(row[1])
        if level_code in postgrad_codes:
            postgrad_list.append(cred_name)
    return postgrad_list