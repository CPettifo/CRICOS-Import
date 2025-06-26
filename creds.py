# This file will process the standardised credential data and convert it into the appropriate WHED Codes
import mysql.connector, os, tempfile
from openpyxl import load_workbook, Workbook

def main():
    # Get list of FOS Codes and FOS Levels / Display Categories from WHED (or spreadsheet)
    # Open connection to the WHED
    conn = whed_connect()
    cursor = conn.cursor(dictionary=True)
    # get test data
    cursor.execute("SELECT GlobalID, OrgName FROM whed_org LIMIT 20;")



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


# will return the conn for the database connection
def whed_connect():
    certificate = os.environ.get("DB_CERT")
    if not certificate:
        raise ValueError("No DB_CERT value found")
    
    # create the ssl file from the ssl contents stored in env variabls
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pem") as ssl_file:
        ssl_file.write(certificate.encode("utf-8"))
        ssl_file_path = ssl_file.name

    # connect to the remote db using env variables and the cert file created above
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),database=os.getenv("DB_NAME"),
        ssl_ca=ssl_file_path,
        port=int(os.getenv("DB_PORT", 3306))
    )
    return conn