import re

def normalize_uz_phone(value: str) -> str:
    if not value:
        return value

    # faqat raqamlarni qoldiramiz
    digits = re.sub(r'\D', '', value)

    # 9 xonali bo‘lsa (901234567)
    if len(digits) == 9:
        return '+998' + digits

    # 12 xonali bo‘lsa (998901234567)
    if len(digits) == 12 and digits.startswith('998'):
        return '+' + digits

    # 13 xonali bo‘lsa (+998901234567)
    if len(value) == 13 and value.startswith('+998'):
        return value

    raise ValueError("Noto‘g‘ri telefon format")


import re
from django.core.exceptions import ValidationError

def validate_uz_phone(value):
    pattern = r'^\+998\d{9}$'

    if not re.match(pattern, value):
        raise ValidationError(
            "Telefon raqam +998901234567 formatda bo‘lishi kerak"
        )