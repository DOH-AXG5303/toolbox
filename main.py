import string
import random
import hashlib




def padding_gen():
    """
    Generate a string of random length between 0 and 3000 characters
    to be used as padding for API calls
    
    return:
        string 
    """
    
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    length = random.randint(0,3000)
    
    return "".join([random.choice(chars) for i in range(length)])




def uuid_gen(text, salt = "HMAC_key"):
    """
    Generate a hash (uuid) from phone number string and HMAC key (unique passphrase)
    MD5 hash algorithm 
    
    return:
        string
    """
    textutf8 = text.encode("utf-8")
    saltutf8 = salt.encode("utf-8")
    
    hash_key = hashlib.md5(saltutf8+b":"+textutf8)
    hexa = hash_key.hexdigest()
    
    return hexa
    