import inspect

# Use this to mark a function as deprecated that you are too lazy to remove atm
# tells you: the name of the function
#            the name of the function that called that function
#            an optional message for reasoning or whatever you want
def __deprecated__(str_msg_optional = ""):
    print("--- Warning, use of deprecated function ---")
    print(inspect.stack()[1].function)
    print("called from: " + str(inspect.stack()[2].function))
    if str_msg_optional != "":
        print("Message: " + str_msg_optional)
