import random
import array
import string
from cryptography.fernet import Fernet
from .cipher import get_key
from .hashing import get_full_salt


def get_data_for_password(separate: bool = True):
    digits = string.digits
    lower_case_letters = string.ascii_lowercase
    upper_case_letters = string.ascii_uppercase
    symbols = string.punctuation

    if separate:
        return digits, lower_case_letters, upper_case_letters, symbols

    return digits + lower_case_letters + upper_case_letters + symbols


def generate_new_password(pass_phrase: str, __pass_phrase__: str, __data__: list, password_length: int = 16):

    digits, lower_case_letters, upper_case_letters, symbols = get_data_for_password()

    rand_digit = random.choice(digits)
    rand_lower = random.choice(lower_case_letters)
    rand_upper = random.choice(upper_case_letters)
    rand_symbol = random.choice(symbols)

    temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol
    temp_pass_list = []

    for x in range(password_length - 4):
        temp_pass = temp_pass + random.choice(get_data_for_password(separate=False))

        temp_pass_list = array.array('u', temp_pass)

        random.shuffle(temp_pass_list)

    new_password = ""
    for x in temp_pass_list:
        new_password = new_password + x

    if not check_if_password_unique(pass_phrase, __pass_phrase__, __data__, new_password):
        new_password = generate_new_password(pass_phrase, __pass_phrase__, __data__, password_length)

    return new_password


def check_if_password_unique(pass_phrase: str, __pass_phrase__: str, __data__: list, new_password: str):

    salt = get_full_salt(pass_phrase, __pass_phrase__)

    coder = Fernet(get_key(pass_phrase, salt))

    for password_element in __data__:

        password = coder.decrypt(password_element.password).decode('utf-8')

        if password == new_password:
            return False

    return True
