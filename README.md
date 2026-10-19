# pwCheck
Scores password strength, checks if password was found in known data leaks, and generates strong passwords.


This is a command line tool I built in Python that checks how strong a password is, checks if its been leaked in a data breach, and can generate a strong password and passphrase. 

# What it does:
- Checks a passwords strength and tellsl you what's wrong with it   
    - too short
    - repeated chars
    - simple sequences 
    - only one type of char
    - a really common password
- Checks if a password has been in a data breach
    - uses the Have I Been Pwned database
- Generates passwords and passphrases that are actually random

# How to run:
- you need Python 3.9 or newer
- Run:
    - git clone https://github.com/SophieCastetb/pwCheck.git
    - cd pwCheck
    - python -m pip install -e

- Then Run:
    - python -m pwCheck check       # check a password (what you type stays hidden)
    - python -m pwCheck check --no-breach      # skip the online breach check
    - python -m pwCheck generate     # make a random 16 character password
    - python -m pwCheck generate --length 24 --no-symbols
    - python -m pwCheck generate --passphrase --words 5
    - python -m pwCheck --help       # see all the options

- An example from my own program output is using the password "Hello123!"
    - PS C:\Users\sophi\OneDrive\Personal Projects\pwCheck> python -m pwCheck check
    - Enter password: 
    - Rating: fair
    - Entropy: 59.0bits
    - WARNING: found in (73964,)known data breachs. Don't use it

- Another example from my own program output while using the password "x7E2i&&3."
    - PS C:\Users\sophi\OneDrive\Personal Projects\pwCheck> python -m pwCheck check
    - Enter password: 
    - Rating: fair
    - Entropy: 59.0bits
    - Not found in known data breaches

# How Breach check works:
- I was think about not sendigng your password anywhere just in case it is sensitive information (and also in real life it's definetly sensitive information) so I used something called k-anonymity
- k-anonymity
    - your own computer turns the password into SHA-1 hash 
    - then only the first 5 chars are send to the API (of the hash)
    - The API will send back a list of every leaked hash that starts with those 5 chars
    - and then the computer will check if any of them match yours
- this is so the full password never actually leaves your computer

# How Strength check works
- It estimates entropy (which means how hard a password is to guess) by using length x log2(poolsize) where poolsize depends on which kidns of chars are in the password
    - in my case i choise lowercase, uppercase, digits, and symbols
- I also had it check for repeated characters, sequences, and only one type of character, and also a list of common passwords

- passwords are either weak, fair, or strong

# Important notes (things people I talked to advised me to do):
- used the secrets module instead of random for the generator
    - I was told that random isn't really meant to be secure
- getpass : used it so what you're typing doesn't show on screen or in the terminal history
- passphrases use the EFF wordlist so a 4 word passphrase is about 51 bits of entropy
- if ur offline it tells you the breach check was skipped instead of crashing the program

# What I might want to add later
- catching word tricks like @ used as a or 0 used as O (p@ssw0rd)
- catching better sequences cause right now it only catches runs
- maybe a web version that is simple and easy to use

# Websites or Databases I used
- Breach data from Have I Been Pwned
- Wordlist from the EFF