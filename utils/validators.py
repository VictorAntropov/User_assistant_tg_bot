import re

from constants.information import (PROJECT_CHECK_NAME, PROJECT_CHECK_PHONE,
                                   PROJECT_CHECK_S_NAME, PROJECT_EMAIL_MISTAKE,
                                   PROJECT_VALID_ADDRESS)

pattern_number = (r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]'
                  r'?[0-9]{2}[\s\-]?[0-9]{2}$')
pattern_name = r'^[А-ЯЁ][а-яё]*$'
pattern_address = r'(^[A-Za-zА-Яа-я]*$)'
pattern_email = r'[0-9A-Za-z]+@[a-zA-Z]+\.(com|net|org|ru)$'


def getting_user_info(full_name):

    full_name = list(full_name.split(' '))
    number = validate_info(pattern_number, full_name[2])
    name = validate_info(pattern_name, full_name[1])
    s_name = validate_info(pattern_name, full_name[0])

    if not number:
        raise ValueError(PROJECT_CHECK_PHONE)
    if not name:
        raise ValueError(PROJECT_CHECK_NAME)
    if not s_name:
        raise ValueError(PROJECT_CHECK_S_NAME)
    else:
        return full_name[1], full_name[0], full_name[2]


def getting_user_address_company(full_info):
    full_info = list(full_info.split(' '))
    address = validate_info(pattern_address, full_info[-1])
    company = full_info[:len(full_info)-1]

    if not address:
        raise ValueError(PROJECT_VALID_ADDRESS)
    else:
        return ' '.join(company), full_info[-1]


def check_user_email(email):
    email_check = validate_info(pattern_email, email)
    if not email_check:
        raise ValueError(PROJECT_EMAIL_MISTAKE)
    else:
        return email


def validate_info(pattern, argument):
    match = re.match(pattern, argument)
    if match:
        return True
    else:
        return False
