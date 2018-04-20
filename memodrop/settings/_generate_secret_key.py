import random
import string


def generate_secret_key(length=50):
    chars = ''.join([
        string.ascii_letters,
        string.digits,
        string.punctuation
    ]).replace('\'', '').replace('"', '').replace('\\', '')

    return ''.join([random.SystemRandom().choice(chars) for _ in range(length)])
