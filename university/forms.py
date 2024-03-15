
from django import forms

from .models import BookingReviewer


class BookingReviewerForm(forms.ModelForm):
    
    class Meta:
        model = BookingReviewer
        fields = ("first_name", 'last_name', 'phone', 'address',
                    'gender', 'university', 'salary', 'is_working'
                    )

