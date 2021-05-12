import random
import string
from core.models import *
import hashlib, binascii, os


def get_short_url():
    short_url = ''.join(random.SystemRandom().choice(
        string.ascii_letters + string.digits) for _ in range(7))
    result = url_collection.find_one({"short_url": short_url})
    if(result != None):
        get_short_url()
    else:
        return short_url

def get_unique_user_id():
    user_id = ''.join(random.SystemRandom().choice(
        string.ascii_letters + string.digits + "_&*" ) for _ in range(7))
    result = user_collection.find_one({"_id": user_id})
    if(result != None):
        get_unique_user_id()
    else:
        return user_id

def get_unique_session_id():
    session_id = ''.join(random.SystemRandom().choice(
        string.ascii_letters + string.digits + "_&*" ) for _ in range(10))
    result = session_collection.find_one({"_id": session_id})
    if(result != None):
        get_unique_session_id()
    else:
        return session_id

def get_password_hash(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  password.encode('utf-8'), 
                                  salt, 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def check_custom_slug_availability(custom_slug):
    result = url_collection.find_one({"short_url": custom_slug})
    if(result != None):
        return False
    else:
        return True


