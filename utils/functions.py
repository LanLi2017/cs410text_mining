from itertools import chain
import os
import random
import re
import string

from django.core.management.utils import get_random_secret_key


def load_secret_key(file):
    if not os.path.exists(file):
        secret_key = get_random_secret_key()
        with open(file, 'wt') as f:
            f.write(secret_key)
        return secret_key
    else:
        with open(file, 'rt') as f:
            return f.read()


def random_token(length=64, character_set=None):
    if character_set is None:
        character_set = [
            string.ascii_uppercase,
            string.ascii_lowercase,
            string.digits,
        ]
    character_set = list(chain.from_iterable(character_set))
    return ''.join(random.choice(character_set) for _ in range(length))


# https://stackoverflow.com/questions/46155/how-can-you-validate-an-email-address-in-javascript
email_pattern = re.compile(
    r'^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@'
    r'((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])'
    r'|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
)


def normalize_email(email):
    email = email.lower().strip()

    if email_pattern.fullmatch(email) is None:
        email = ''

    return email
