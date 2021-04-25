import random
import string
import models 
from models import *


def get_short_url():
    short_url = ''.join(random.SystemRandom().choice(
        string.ascii_letters + string.digits) for _ in range(7))
    result = collection.find_one({"short_url": short_url})
    if(result != None):
        get_short_url()
    else:
        return short_url
