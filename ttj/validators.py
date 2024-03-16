from django.core.exceptions import ValidationError

def validate_admission_by_bed_status(status):
        # (0, "Joy qolmagan"),
        # (1, "Foydalanishga berilmagan"),
        # (2, "Bo'sh"),
        # (3, "Bo'sh joylar bor")
    if status not in (2, 3):
        raise ValidationError(f"Tanlanayotgan xonaga qo'shib bo'lmaydi\nChunki uning statusi:{status} ")


def validate_admission_by_ttj_capacity(ttj:object):
    if ttj.capacity >= ttj.get_all_students_in_ttj():
        raise ValidationError(f"TTJ da joy qolmagan...")


def validate_admission_by_student_approvement(student:object):
    if not student.approved:
        raise ValidationError(f"Ushbu studentning TTJ uchun arizasi tasdiqlanmagan")


def validate_changing_bed_status(bed:object):
    if bed.status in (1, 2) and bed.admission_set.filter(status=1).exists():
        raise ValidationError(f"Siz yotoqning statusini {bed.get_str_status()} ga o'zgartiraolmaysiz chunki ushbu xonada talabalr yashamoqda")
        