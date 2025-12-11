import re

class Validator:
    @staticmethod
    def validate_phone(phone):
        return re.match(r'^\+91[6-9]\d{9}$', phone)
