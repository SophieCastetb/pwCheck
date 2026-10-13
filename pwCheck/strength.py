import math
import re


#Entropy estimates how hard a password is to guess : length * log2(pool size)
#Pool size used : 
    #uppercase letters: 26
    #lowercase letters: 26
    #symbols : 32
    #digits: 10
def  calculate_entropy(password):
    #figuring out pool size
    poolSize = 0
    if any(char.isupper() for char in password):
        poolSize += 26
    if any(char.islower() for char in password):
        poolSize += 26
    if any(char.isdigit() for char in password):
        poolSize +=10
    if any(not char.isalnum() for char in password):
        poolSize += 32

    if poolSize == 0:
        return 0.0,0 

    #calculating entropy value
    entropy_val = 0
    entropy_val = len(password) * math.log2(poolSize)

    return entropy_val, poolSize



#checks to see if passwords are strong
    
#length
def checkLength(password):
    if len(password) <= 8: 
        return True
    return False

#repeated letters
def checkRepeat(password):
    if bool(re.search(r'(.)\1\1',password)):
        return True
    return False

#Sequences
def checkSequences(password):
    if re.findall(r"\d{4}", password):
        return True
    return False

#Character type
def checkPoolSize(password):
    entropy, poolSize = calculate_entropy(password)
    if poolSize == 26 or poolSize ==10 or poolSize == 32:
        return True
    return False


def evaluate_Password(password):
    entropy, poolSize = calculate_entropy(password)

    #issues 
    issues = []
    if (checkLength(password)):
        issues.append( "Password less than 8 characters")
    if (checkRepeat(password)):
        issues.append("Symbol repeats 3 times")
    if (checkSequences(password)):
        issues.append("There's a sequence")
    if (checkPoolSize(password)):
        issues.append("Only one character type")

    #threshold
    if (entropy <= 40):
        rating = "weak"

    if (entropy > 40 and entropy <= 60):
        rating = "fair"

    if (entropy > 60):
        rating = "strong"

    return {"entropy": entropy, "rating": rating, "issues": issues}   
