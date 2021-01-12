import random
import string


# tracking number
def generate_code(digits=8):
    key = "".join(random.choices(string.ascii_uppercase + string.digits, k=digits))
    return key
