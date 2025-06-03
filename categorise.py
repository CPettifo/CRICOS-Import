# CRICOS is an Australian Credential Registry that does not have an API, they do however regularly export from their database and release exports to the public as excel spreadsheets.
# The World Higher Education Database (WHED) aims to catalogue every higher education institution in the world including institutional and credential information.

# The purpose of this script is to process the data within the CRICOS exports and import it directly into the WHED to semi-automate the update process for Australia.


# Before the process begins the latest list of WHED-recognised institutions in Australia is exported with their ID and added as a sheet in the masterlist

def main():
        

    ###Initialise Variables###
    # WHED-Recognised Institutions not recognised by CRICOS
    whed_check = 0

    # WHED-Candidates within CRICOS
    whed_candidates = 0

    # Non WHED-Level Institutions
    whed_excluded = 0

    ###Initialise Lists###

    # List of Level Codes that are considered post-grad by the WHED
    postgrad_codes = ["6C", "7A", "7B", "7C", "7D"]

    # List of credential titles from the spreadsheet (this could later be turned into a query by )
    postgrad_list = get_postgrad_list()


    # Read masterlist




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



#TODO Flesh out this function
# Checks the credentials offered at a specific institution to see if it is a possible WHED candidate
def whed_check():
    return 0


# Prints a summary of the categorisation process in the terminal
def output_summary():
    return 0


# Takes the list of postgrad codes as input and compares all credentials in the whed_levels sheet
def get_postgrad_list(postgrad_codes):
    postgrad_list = []
    # open masterlist

    # for row of credential name

        # if column 2 in postgrad_codes:
            #postgrad_list.append(name of cred)

    return postgrad_list