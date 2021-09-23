import hashlib, binascii, os

# This function receives a password as a parameter
# its hashes and salts using sha512 encoding
def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

# below provide a plain password and see its hashed/salted output
# hashedpassword = hash_password("modcom2020")
# print(hashedpassword)
#
# we use sha512 algorithm
# this function checks if hashed password is the same as
# provided password
def verify_password(hashed_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = hashed_password[:64]
    hashed_password = hashed_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == hashed_password
# run it , provide the hashed and the real password
# SHOULD GIVE YOU TRUE/FALSE
status = verify_password('80ef0c08a1796e515fc5b2b4af1ef9e867552b41f24f12a599ad95976b26483fabc0a6cc20b190bef31f7b1299f5fb71702f3ad00cf23cb954e09a2a142778467700345967ddb186879983a6be1de54a8bbc9802c2e9306c3b7c1c27a08647f2', "j2TLCk")
print(status)