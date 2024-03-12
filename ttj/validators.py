from django.core.exceptions import ValidationError

def validate_admission_by_bed_status(status):
        # (0, "Joy qolmagan"),
        # (1, "Foydalanishga berilmagan"),
        # (2, "Bo'sh"),
        # (3, "Bo'sh joylar bor")
    if status not in (2, 3):
        return ValidationError(f"Tanlanayotgan xonaga qo'shib bo'lmaydi")
  