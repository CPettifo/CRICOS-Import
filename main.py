import categorise # type: ignore

masterlist_path = "masterlist.xlsx"
glossary_path = "glossary.xlsx"


# Ask for user input if categorisation is required
# user_input = input("categorise institutions? [Y/ N]: ")

user_input = "Y"

if user_input == "Y":
    # Categorise institutions (WHED-Recognised, WHED-Candidate, etc.)
    categorise.main(glossary_path)


print("Continuing")