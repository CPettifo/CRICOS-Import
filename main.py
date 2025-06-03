import categorise # type: ignore

masterlist_path = "masterlist.xlsx"


# Ask for user input if categorisation is required
user_input = input("categorise institutions? [Y/ N]")

if user_input == "Y":
    # Categorise institutions (WHED-Recognised, WHED-Candidate, etc.)
    categorise.main(masterlist_path)


print("Continuing")