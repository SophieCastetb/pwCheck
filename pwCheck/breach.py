import hashlib
import requests


def hash_password(password):
    return hashlib.sha1(password.encode("utf-8")).hexdigest().upper()


def find_suffix(response_text, suffix):
    """Search the API's response for our hash suffix. Returns breach count (0 if not found)."""
    for line in response_text.splitlines():
        hash_suffix, _, count = line.partition(":")
        if hash_suffix.strip() == suffix:
            return int(count)
    return 0


def check_breach(password):
    if not password:
        return {"breached": None, "count": 0, "error": "Empty password"}

    sha1 = hash_password(password)
    prefix, suffix = sha1[:5], sha1[5:]

    try:
        response = requests.get(
            f"https://api.pwnedpasswords.com/range/{prefix}", timeout=5
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        return {"breached": None, "count": 0, "error": "Breach database timed out"}
    except requests.exceptions.RequestException:
        return {"breached": None, "count": 0, "error": "Could not reach breach database"}

    count = find_suffix(response.text, suffix)
    return {"breached": count > 0, "count": count}
