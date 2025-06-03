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
    
    # Open the CRICOS institution sheet
    cricos_inst = wb['cricos_inst']
    
    # Open the courses sheet
    cricos_cred = wb['cricos_cred']

    # Open the WHED institution sheet
    whed_inst = wb['whed_inst']


    # For each institution
    for row in cricos_inst.iter_rows(min_row=2, values_only = True):
        # Offers >= Bachelor Honours, these are WHED candidates (will have to check whether they have a certain number of graduate cohorts)
        
        # insts are by default excluded 
        inst = {
        "whed_id": None,
        "whed_name": None,
        "whed_match_type": None,
        "cricos_id": str(row[0]),
        "cricos_name": str(row[2]),
        "cricos_trading": str(row[1]),
        "status": "excluded",
        "match_type": None
        }
        
        # and have their status changed to candidate within the candidate_check function
        inst = candidate_check(inst, postgrad_list, cricos_cred)
        


        # check whether the institution is in the WHED and update the dict as appropriate
        inst = whed_check(inst, whed_inst)
        
        insts.append(inst)



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


    # Write output with:
    # appropriate WHED OrgIDs added to matched institutions
    # institution dicts in excel format to allow for later verification by Data Officers
    # wb.save("output.xlsx")


#TODO Flesh out this function
# Checks the credentials offered at a specific institution to see if it is a possible WHED candidate, takes the institution dict, the cred list, and the cred ws as input
def candidate_check(inst, cred_list, cricos_cred):
    # loop through all credentials in the list
    for row in cricos_cred.iter_rows(min_row = 2, values_only = True):
        cricos_id = str(row[0])
        # If the current credential is offered at the institution being checked, get the credential type
        if inst["cricos_id"] == cricos_id:
            cred_type = str(row[12])
            expired = str(row[23])
            # If the credential type is in the list of postgrad types and it's not expired, the institution is WHED candidate
            if cred_type in cred_list and expired == "No":
                inst["status"] = "candidate"
                return inst
    return inst


# Will try to match institutions in CRICOS to an export from the WHED and will return the instituion name, id, and match type (name, site, address) if it matches
# Takes the institution dict and the whed_institution sheet as input
def whed_check(inst, whed_inst):
    for row in whed_inst:
        #Placeholder
        foobar = "z"
        # if webpages match
        if foobar:
            inst["match_type"] = "web"
        # if street addresses match
        elif foobar:
            inst["match_type"] = "address"
        # if names match
        elif foobar:
            inst["match_type"] = "name"
    
    # If there weas a match, congrats it's a confirmed whed institution
    if inst["match_type"] != None:
        inst["status"] = "confirmed"
    # Otherwise it needs to be flagged for verification by Data Officers
    else:
        inst["status"] = "verify"
    return inst

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