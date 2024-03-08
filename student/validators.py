from django.core.exceptions import ValidationError

def validate_payment_amount(amount):
    if amount <= 0:
        raise ValidationError(f"To'lov miqdori 0 UZS dan katta bo'lishligi taminlansin!")


def validate_doing_payment(student):
    if not student.approved:
        raise ValidationError(f"Ushbu talaba ttj ga to'lov qilaolishi uchun avval TTJ ga qabul qilinishi kerak")
