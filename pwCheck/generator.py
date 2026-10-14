import secrets
import string
from pathlib import Path

#have the EFF long wordlist downloaded but this is a fallback
DEFAULT_WORDS = ["anchor", "bridge", "candle", "dragon", "ember",
                 "forest", "garden", "harbor", "island", "jungle", 
                 "kettle", "lantern", "meadow", "nebula", "orchard", 
                 "pepper", "quartz", "river", "saddle","thunder",
                 "umbrella", "velvet", " walnut", "yonder","zephyr", 
                 "marble", "copper","falcon", "glacier","horizon", 
                 "indigo", "juniper"]

WORDLIST_PATH= Path(__file__).parent / "wordlist.txt"

def load_wordlist():
    if WORDLIST_PATH.exists():
        words = WORDLIST_PATH.read_text(encoding="utf-8").split()
        if words:
            return words
        return DEFUALT_WORDS

length = 16
use_symbols = True
def generate_password():
    if length < 8:
        raise ValueError("Password length must be at least 8")
    #one pool per char type so we can guarantee each type appears
    pools = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
    if use_symbols:
        pools.append(string.punctuation)
    alphabet = "".join(pools)

    chars = [secrets.choice(pool) for pool in pools]
    chars += [secrets.choice(alphabet) for _ in range(length - len(chars))]
    #shuffle so the guaranteed cahracters aren't always at the front of the password
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)

words = 4
separator = "-"
def generate_passphrase():
    if words <3:
        raise ValueError("Password needs at least 3 words")
    wordlist= load_wordlist()
    return separator.join(secrets.choice(wordlist)for _ in range(words))