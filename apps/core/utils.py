import logging

import phonenumbers

log = logging.getLogger(__name__)


def normalize_phone(phone: str, region: str = None) -> str:
    """
    Метод нормализует номер телефона, приводя его в единый формат проекта.
    """
    phone = phone[:] if phone and isinstance(phone, str) else ""

    value = phone.strip() if "+" in phone else "+" + phone.strip()
    value = value.replace("+8", "+7").replace("+9", "+79")
    try:
        phone = phonenumbers.parse(value, region)

        return phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
    except Exception as err:
        log.error(f"normalize_phone; Error={err}")
        return phone
