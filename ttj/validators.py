from django.core.exceptions import ValidationError

def validate_admission_by_bed_status(status):
        # (0, "Joy qolmagan"),
        # (1, "Foydalanishga berilmagan"),
        # (2, "Bo'sh"),
        # (3, "Bo'sh joylar bor")
    if status not in (2, 3):
        raise ValidationError(f"Tanlanayotgan xonaga qo'shib bo'lmaydi")


def validate_admission_by_ttj_capacity(ttj:object):
    if ttj.capacity >= ttj.get_all_students_in_ttj():
        raise ValidationError(f"TTJ da joy qolmagan...")


def validate_admission_by_stuent_approvement(student:object):
    if not student.approved:
        raise ValidationError("Ushbu studentning TTJ uchun arizasi tasdiqlanmagan")
