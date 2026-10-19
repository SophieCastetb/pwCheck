import secrets
import string
from pathlib import Path

#the EFF long wordlist is downloaded but this is a fallback
DEFAULT_WORDS = ["anchor", "bridge", "candle", "dragon", "ember",
                 "forest", "garden", "harbor", "island", "jungle", 
                 "kettle", "lantern", "meadow", "nebula", "orchard", 
                 "pepper", "quartz", "river", "saddle","thunder",
                 "umbrella", "velvet", " walnut", "yonder","zephyr", 
                 "marble", "copper","falcon", "glacier","horizon", 
                 "indigo", "juniper"]

WORDLIST_PATH= Path(__file__).parent / "wordlist.txt"
#reads word list or falls back on DEFAULT_WORDS
def load_wordlist():
    if WORDLIST_PATH.exists():
        words = WORDLIST_PATH.read_text(encoding="utf-8").split()
        if words:
            return words
        return DEFAULT_WORDS

#makes a random password . 
#secrets is used instead of random cause operating system's secure random source
length = 16
use_symbols = True
def generate_password(length= 16, use_symbols=True):
    if length < 8:
        raise ValueError("Password length must be at least 8")
    #one pool per char type so we can guarantee each type appears
    pools = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
    if use_symbols:
        pools.append(string.punctuation)
    alphabet = "".join(pools)
    #one guaranteed char from each pool, fill rest up with all 
    chars = [secrets.choice(pool) for pool in pools]
    chars += [secrets.choice(alphabet) for _ in range(length - len(chars))]
    #shuffle so the guaranteed cahracters aren't always at the front of the password
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)

words = 4
separator = "-"
#makes passpharse of random words
def generate_passphrase(words=4, separator="-"):
    if words <3:
        raise ValueError("Password needs at least 3 words")
    wordlist= load_wordlist()
    return separator.join(secrets.choice(wordlist)for _ in range(words))