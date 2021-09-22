'''
Random Password Generator using Python
Author: Ayushi Rawat
'''

#import the necessary modules!
import random
import string


def password_generator():
    #input the length of password
    length = 6
    #define data
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    #string.ascii_letters
    #combine the data
    all = lower + upper + num
    #use random
    temp = random.sample(all,length)
    #create the password
    password = "".join(temp)
    #print the password

    return password







