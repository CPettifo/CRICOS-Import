from openpyxl import load_workbook #type: ignore
import os

# CRICOS is an Australian Credential Registry that does not have an API, they do however regularly export from their database and release exports to the public as excel spreadsheets.
# The World Higher Education Database (WHED) aims to catalogue every higher education institution in the world including institutional and credential information.

# The purpose of this script is to process the data within the CRICOS exports and import it directly into the WHED to semi-automate the update process for Australia.


# Before the process begins the latest list of WHED-recognised institutions in Australia is exported with their ID and added as a sheet in the masterlist

# The main method is called by the main.py script
def main(masterlist_path, postgrad_codes):
    # open masterlist
    if not os.path.exists(masterlist_path):
        print(f"File not found {masterlist_path}")
        return

    # Read masterlist
    print("Opening masterlist be patient this takes a sec...", flush = True)
    wb = load_workbook(masterlist_path)
    

    # open the whed_levels sheet
    whed_levels = wb['whed_levels']

    # Open the CRICOS institution sheet
    ext_inst = wb['ext_inst']
    
    # Open the courses sheet
    ext_cred = wb['ext_cred']

    # Open the WHED institution sheet
    whed_inst = wb['whed_inst']


    ###Initialise Lists & Dicts###

    insts = []


    # We want the list of postgrad titles (e.g. for CRICOS a Bachelor is 6B, Honours is 6C, etc.)
    print("Checking postgrad degrees")
    postgrad_list = get_postgrad_list(postgrad_codes, whed_levels)

    print(f"List of postgrad credentials offered in this country:\n{postgrad_list}")  


    # For each institution
    for row in ext_inst.iter_rows(min_row=2, values_only = True):
        row_index = row[0]
        # insts are by default ineligible 
        inst = {
        "whed_id": None,
        "whed_name": None,
        "ext_id": str(row[1]),
        "ext_name": str(row[2]),
        "ext_trading": str(row[3]),
        "status": "ineligible",
        "whed_status": None,
        "match_type": None
        }

        inst_supp = {
            "ext_url": str(row[4]),
            "ext_address": str(row[5])
        }
        print(f"Row {row_index}")
        print(inst['ext_name'], flush = True)
        
        inst = candidate_check(inst, postgrad_list, ext_cred)

        # check whether the institution is in the WHED and update the dict as appropriate
        inst = whed_check(inst, inst_supp, whed_inst)
        
        print(f"Candidate status: {inst['status']}\n\n")

        insts.append(inst)



    whed_candidates = 0
    whed_ineligible = 0
    whed_verify = 0
    whed_confirmed = 0
    whed_address = 0

    print("----------List of ineligible institutions----------")
    for inst in insts:
        if(inst["status"] == "ineligible"):
            print(inst["ext_name"])
            whed_ineligible += 1

    print("----------List of confirmed institutions---------")
    for inst in insts:
        if(inst["whed_status"] == "confirmed"):
            print(inst["ext_name"])
            whed_confirmed += 1

    print("----------List of Potential WHED Candidates----------")
    for inst in insts:
        if(inst["status"] == "candidate"):
            print(inst["ext_name"])
            whed_candidates += 1

    print("----------List of institutions to check validity-----")
    for inst in insts:
        if(inst["status"] == "verify"):
            print(inst["ext_name"])
            whed_verify += 1

    print("----------List of institutions with partial address matches-----")

    print("Analysis complete (for details scroll up)")
    print(f"Potential WHED level candidates: {whed_candidates}")
    print(f"Ineligible instititions based on degree offerings: {whed_ineligible}")
    print(f"Institutions in WHED that are do not offer postgrad according to CRICOS: {whed_verify}")
    print(f"WHED institutions confirmed by CRICOS: {whed_confirmed}")
    print(f"Institutions with partial (or full) address matches: {whed_address}")

    print("Writing to output.xlsx, stand by")

    # write institutions to excel format to allow for later verification by Data Officers
    write_output(insts)


# Checks the credentials offered at a specific institution to see if it is a possible WHED candidate, takes the institution dict, the cred list, and the cred ws as input
def candidate_check(inst, cred_list, ext_cred):
    # loop through all credentials in the list
    for row in ext_cred.iter_rows(min_row = 2, values_only = True):
        ext_id = str(row[0])
        # If the current credential is offered at the institution being checked, get the credential type
        if inst["ext_id"] == ext_id:
            cred_type = str(row[3])
            expired = str(row[2])
            # If the credential type is in the list of postgrad types and it's not expired, the institution is WHED candidate
            if cred_type in cred_list and expired == "No":
                inst["status"] = "candidate"
                return inst
    return inst


# Will try to match institutions in CRICOS to an export from the WHED and will return the instituion name, id, and match type (name, site, address) if it matches
# Takes the institution dict and the whed_institution sheet as input
def whed_check(inst, inst_supp, whed_inst):
    # For clarity and sanity I mapped the dict to a local variable, the same is done for each whed institution below
    ext_name = inst["ext_name"]
    ext_name_alt = inst["ext_trading"]
    ext_url = inst_supp["ext_url"]
    ext_address = inst_supp["address"]



# "whed_id": None,
#"whed_name": None,
# "status": "ineligible",
# "whed_status": None,
# "match_type": None

    for row in whed_inst:
        whed_id = str(row[0])
        whed_name = str(row[2])
        whed_name_eng = str(row[3])
        whed_name_alt = str(row[4])
        whed_url = str(row[5])
        whed_address = str(row[6])





        #Placeholder
        foobar = "z"
        # if webpages match
        if foobar == 'w':
            # Replace http://, https://, www. with "" for both ext and whed and compare
            inst["match_type"] = "web"
        # if street addresses match, add it to verify with the match_type: address (it's a fuzzy match so will need to be checked)
        elif foobar == 'w':
            inst["match_type"] = "address"
        # if names match
        elif foobar == 'w':
            inst["match_type"] = "name"
    


        # If there was a match link the whed ID and check whether it should remain a WHED candidate
        if inst["match_type"] != None:
            inst["whed_id"] = whed_id
            inst["whed_name"] = whed_name
            if inst["status"] == "candidate":
                inst["status"] = "confirmed"
            else:
                inst["status"] = "verify"


    return inst

# Takes the list of postgrad codes and the whed_levels sheet as input and returns a list of course names at post-grad level
def get_postgrad_list(postgrad_codes, whed_levels):
    # for row of credential name
    for row in whed_levels.iter_rows(min_row=2, values_only = True):
        cred_name = str(row[0])
        level_code= str(row[1])
        if level_code in postgrad_codes:
            # append to the list of NQF codes in case the source spreadsheet uses those instead of names
            postgrad_codes.append(cred_name)
    return postgrad_codes


def write_output(insts):
     
    
    
    # wb.save("output.xlsx")

    return 0