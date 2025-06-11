# This file will process the standardised credential data and convert it into the appropriate WHED Codes




# Get list of WHED confirmed institutions from categorise list or spreadsheet


# Get list of FOS Codes and FOS Levels / Display Categories from WHED (or spreadsheet)


# For each institutions 
    # For each credential
        # If credential's institution matches the one in the loop
            # Match credentials to the appropriate WHED CredCode (e.g. Australian Bachelor has CredCode of ####)

            # Match Field to appropriate whed FOS using the following hierarchy
                # If any of the FOS fields match, use that
                    # Get WHED FOS Code and add it to a dict
                # If a shaved version of the credential name matches a WHED FOS field
                    # Get WHED FOS Code and add it to a dict
                # If there is a fuzzy match
                    # Add the cred to the "to be sorted" category, and add to a bucket
                    # By bucket I mean basically to have all unsorted categories matched together, so there could potentially be 100 instances of a
                    # non-matched field (e.g. Mobile Programming) that could then be categorised by a Data Officer at the end of the program
    
