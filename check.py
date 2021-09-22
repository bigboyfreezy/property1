def check_empty(variable):
    if len(variable)== 0:
        return True
    else:
        return False


import re

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


def check(email):
    if (re.search(regex, email)):
        print("Valid Email")
    else:
        print("Invalid Email")

def check_pass(variable):
    if len(variable) < 8:
        return 'Password Must be more than 8 characters'
    elif not re.search("[a-z]", variable):
        return 'Must have atleast few small characters'
    elif not re.search("[A-Z]", variable):
        return 'Must have atleast few number characters'
    elif not re.search("[0-9]", variable):
        return 'Must have atleast few small characters'
    else:
        return True
