import hashlib

def hashSalt(password):
    salt = b']:\xfb+\x9e\xa8\x9e4\x16\x0eo\x0f;\xd5\xee\xed%\xc7\xe9\xcc/\xeb|J\xed\xcc\xdf\xe7\x01\x01\xcb\xf9'
    passwordHash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 10000)
    hexHash = passwordHash.hex()
    return hexHash