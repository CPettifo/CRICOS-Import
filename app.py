# CRICOS is an Australian Credential Registry that does not have an API, they do however regularly export from their database and release exports to the public as excel spreadsheets.
# The World Higher Education Database (WHED) aims to catalogue every higher education institution in the world including institutional and credential information.

# The purpose of this script is to process the data within the CRICOS exports and import it directly into the WHED to semi-automate the update process for Australia.


# Before the process begins the latest list of WHED-recognised institutions in Australia is exported with their ID and added as a sheet in the masterlist


# Read masterlist



# Categorise CRICOS institutions
# For each institution


    #TODO Create a function that will take as input an institution name, list of credentials for each category

    # Offers <= Bachelor Degrees, these are Not WHED-level

    # Offers >= Bachelor Honours, these are WHED candidates (will have to check whether they have a certain number of graduate cohorts)


    #TODO Create function that takes as input the institution name
    # Same as above but name matches WHED-Recognised institutions


    # Institutions that are WHED-Recognised that do not appear in the CRICOS list will be given a "To Check" value





# Identify relevant columns



# Identify target schema



# 