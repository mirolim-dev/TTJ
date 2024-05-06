from django.core.exceptions import ValidationError

def validate_payment_amount(amount):
    if amount <= 0:
        raise ValidationError(f"To'lov miqdori 0 UZS dan katta bo'lishligi taminlansin!")


def validate_doing_payment(student):
    if not student.approved:
        raise ValidationError(f"Ushbu talaba ttj ga to'lov qilaolishi uchun avval TTJ ga qabul qilinishi kerak")


def validate_student_for_black_list(student):
    if not student.approved:
        raise ValidationError(f"Studentning TTJ da turish arizasi qondirilmagan.")
    elif student.admission_set == None:
        raise ValidationError(f"Student TTJ ga joylashib ulgurmadi")
    elif student.admission_set.last().status == 0:
        raise ValidationError(f"Ushbu talaba ortiq TTJ da turmaydi shuning uchun uni Qora ro'yxatga qo'sha olmaysiz")
    

def validate_student_tracking(student):
    if not student.approved:
        raise ValidationError(f"Studentning TTJ da turish arizasi qondirilmagan.")
    elif student.admission_set == None:
        raise ValidationError(f"Student TTJ ga joylashib ulgurmadi")
    elif student.admission_set.last().status == 0:
        raise ValidationError(f"Ushbu talaba ortiq TTJ da turmaydi shuning uchun uni tracking qilib bo'lmaydi")


