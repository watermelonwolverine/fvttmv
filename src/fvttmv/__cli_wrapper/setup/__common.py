def ask_yes_or_no_question(question: str):
    while True:
        answer = input("{0} (yes, no): ".format(question))
        if answer in ["yes", "y"]:
            return True
        if answer in ["no", "n"]:
            return False
        print("Please enter 'yes' or 'no'.")
