import hashlib


def generate_hash(password: str, salt: str) -> str:
    """
    Generate hash from password using salt
    :param password: password for hashing
    :param salt: salt which used to hash password
    :return: SHA512 hash
    """

    return hashlib.pbkdf2_hmac(
        'sha512',                    # Используемый алгоритм хеширования
        password.encode('utf-8'),    # Конвертируется пароль в байты
        salt.encode('utf-8'),        # Предоставляется соль
        100000                       # Рекомендуется использовать хотя бы 100000 итераций SHA-256
    ).hex()


def get_salt_length(input_value) -> int:
    """
    Returns length of salt for the current pass_phrase
    :param input_value: Current pass_phrase or pass_phrase length
    :return: Length of salt
    """

    def calculate_salt_length(length):
        return int(length / 2 if length % 2 == 0 else (length + 1) / 2) + 10

    if isinstance(input_value, int):
        return calculate_salt_length(input_value)
    else:
        return calculate_salt_length(len(input_value))


def check_equality(entered_pass_phrase: str, __pass_phrase__: str) -> bool:
    """
    Checks if two pass_phrases are equals
    :param entered_pass_phrase: Current entered pass_phrase
    :param __pass_phrase__: PASS_PHRASE in main.py
    :return: True if equals else False
    """

    salt_length = get_salt_length(entered_pass_phrase)

    pass_phrase_hash = __pass_phrase__[salt_length:-salt_length]

    salt = __pass_phrase__[:salt_length] + __pass_phrase__[-salt_length:]

    return pass_phrase_hash == generate_hash(entered_pass_phrase, salt)


def get_full_salt(pass_phrase, pass_phrase_with_salt: str) -> str:
    """
    Return full salt from PASS_PHRASE
    :param pass_phrase: Real pass_phrase or pass_phrase length
    :param pass_phrase_with_salt: pass_phrase digest with salt (PASS_PHRASE)
    :return: Salt
    """
    salt_length = get_salt_length(pass_phrase)
    salt = pass_phrase_with_salt[:salt_length] + pass_phrase_with_salt[-salt_length:]
    return salt

