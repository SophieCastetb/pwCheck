import math
import re
from pathlib import Path

COMMON_PATH =Path(__file__).parent / "common_passwords.txt"

def load_common():
    if COMMON_PATH.exists():
        return set(COMMON_PATH.read_text(encoding="utf-8").lower().split())
    return set()

#laods common passwords
COMMON_PASSWORDS = load_common()
#things to catch when letters are next to each other on the keyboard
KEYBOARD_ROWS = ["qwertyuop", "asdfghjkl", "zxcvbnm", "1234567890"]


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
    p = password.lower()
    for i in range(len(p)-3):
        chunk = p[i:i+4]
        if chunk.isalnum() and all(ord(chunk[j+1])- ord(chunk[j]) == 1 for j in range(3)):
            return True
        if any(chunk in row for row in KEYBOARD_ROWS):
            return True
    return False

#Character type
def checkPoolSize(password):
    entropy, poolSize = calculate_entropy(password)
    if poolSize == 26 or poolSize ==10 or poolSize == 32:
        return True
    return False

#checks if it matches the list 
def checkCommon(password):
    return password.lower() in COMMON_PASSWORDS

#runs all checks and combines them into one result
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
    if (checkCommon(password)):
        issues.append("Common password")

    #threshold
    if (entropy <= 40):
        rating = "weak"

    if (entropy > 40 and entropy <= 60):
        rating = "fair"

    if (entropy > 60):
        rating = "strong"

    #common password is always weak
    if checkCommon(password):
        rating = "weak"
    elif rating == "strong" and issues:
        rating = "fair"
    return {"entropy": entropy, "rating": rating, "issues": issues}   
