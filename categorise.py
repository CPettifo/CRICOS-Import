from openpyxl import load_workbook #type: ignore
import os

# CRICOS is an Australian Credential Registry that does not have an API, they do however regularly export from their database and release exports to the public as excel spreadsheets.
# The World Higher Education Database (WHED) aims to catalogue every higher education institution in the world including institutional and credential information.

# The purpose of this script is to process the data within the CRICOS exports and import it directly into the WHED to semi-automate the update process for Australia.


# Before the process begins the latest list of WHED-recognised institutions in Australia is exported with their ID and added as a sheet in the masterlist

# The main method is called by the main.py script
def main(glossary_path, masterlist_path):
    if not os.path.exists(glossary_path):
        print(f"File not found {glossary_path}")
        return

    # Read glossary
    print(f"Opening glossary: {glossary_path}")
    wb = load_workbook(glossary_path)

    # open the whed_levels sheet
    whed_levels = wb['whed_levels']

    ###Initialise Lists & Dicts###
    insts = []


    # List of Level Codes that are considered post-grad by the WHED
    postgrad_codes = ["6C", "7A", "7B", "7C", "7D"]

    # List of credential titles from the spreadsheet (this could later be turned into a query by )
    print("Checking postgrad degrees")
    postgrad_list = get_postgrad_list(postgrad_codes, whed_levels)

    print(f"List of postgrad credentials offered in this country:\n{postgrad_list}")


    # open masterlist
    if not os.path.exists(masterlist_path):
        print(f"File not found {masterlist_path}")
        return

    # Read masterlist
    print(f"Opening masterlist: {masterlist_path}, be patient this takes a sec...")
    wb = load_workbook(masterlist_path)
    print(f"Masterlist open")
    
    # Open the institution sheet
    cricos_inst = wb['cricos_inst']
    
    # Open the courses sheet
    cricos_cred = wb['cricos_cred']

    # For each institution
    for row in cricos_inst.iter_rows(min_row=2, values_only = True):
        # Offers >= Bachelor Honours, these are WHED candidates (will have to check whether they have a certain number of graduate cohorts)
        inst = {
        "whed_id": None,
        "whed_name": None,
        "cricos_id": str(row[0]),
        "cricos_name": str(row[2]),
        "cricos_trading": str(row[1]),
        "status": None
        }
        
        if(candidate_check(inst, postgrad_list, cricos_cred)):
            inst["status"] = "candidate"

        # Else whed_excluded
        else:
            inst["status"] = "excluded"

        insts.append(inst)

        #TODO Create function that takes as input the institution name and compares it to the WHED names, addresses or websites
        # Same as above but name matches WHED-Recognised institutions
        # whed_confirmed.append(inst_name)


        # Add column for excluded categories, 
        # in CRICOS but not WHED-level (i.e. doesn't offer Honours+)


        # Not in CRICOS or name mismatch
        # whed_verify.append(inst_name)

    # Save output with appropriate WHED OrgIDs added to matched institutions
    # wb.save("output.xlsx")


    whed_candidates = 0
    whed_excluded = 0
    whed_verify = 0
    whed_confirmed = 0

    print("----------List of excluded institutions----------")
    for inst in insts:
        if(inst["status"] == "excluded"):
            print(inst)
            whed_excluded += 1

    print("----------List of confirmed institutions---------")
    for inst in insts:
        if(inst["status"] == "confirmed"):
            print(inst)
            whed_confirmed += 1

    print("----------List of Potential WHED Candidates----------")
    for inst in insts:
        if(inst["status"] == "candidate"):
            print(inst)
            whed_candidates += 1

    print("----------List of institutions to check validity-----")
    for inst in insts:
        if(inst["status"] == "verify"):
            print(inst)
            whed_verify += 1

    print("Analysis complete (for details scroll up)")
    print(f"Potential WHED level candidates: {whed_candidates}")
    print(f"Excluded instititions based on degree offerings: {whed_excluded}")
    print(f"Institutions in WHED that are do not offer postgrad according to CRICOS: {whed_verify}")
    print(f"WHED institutions confirmed by CRICOS: {whed_confirmed}")


#TODO Flesh out this function
# Checks the credentials offered at a specific institution to see if it is a possible WHED candidate
def candidate_check(inst_name, cred_list, cricos_cred):
    print(inst_name)
    return True

def whed_check(inst_name):
    return 1

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