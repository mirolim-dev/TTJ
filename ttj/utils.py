import io
import qrcode
from PIL import ImageDraw, ImageFont
from django.core.files.base import ContentFile

def generate_qr(student: object):
    # Get the text for the QR code
    json_data = {
        'student_id': student.id,
        'university_id': student.university.id,
        'ttj_id': student.admission_set.first().room.ttj,
    }
    image_name = f"{student.first_name} | {student.last_name}.png"
    custom_text = f"{student.first_name} | {student.last_name} | {student.admission_set.last().room.ttj.name}"
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(json_data)
    qr.make(fit=True)

    # Create an image from the QR code
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Draw custom text on the image
    draw = ImageDraw.Draw(qr_image)
    font = ImageFont.truetype("arial.ttf", 16)  # Adjust font size and style as needed
    draw.text((10, 10), custom_text, fill="black", font=font)

    # Convert image to bytes
    image_bytes = io.BytesIO()
    qr_image.save(image_bytes, format='PNG')
    image_bytes.seek(0)

    # Return the content file
    return ContentFile(image_bytes.getvalue(), name=image_name)
