from django import forms
from .models import ContactMessage

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", "email", "phone", "subject", "message")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "आपका नाम"}),
            "email": forms.EmailInput(attrs={"placeholder": "आपका ईमेल (वैकल्पिक)"}),
            "phone": forms.TextInput(attrs={"placeholder": "मोबाइल नंबर"}),
            "subject": forms.TextInput(attrs={"placeholder": "संपर्क का विषय"}),
            "message": forms.Textarea(attrs={"placeholder": "अपना संदेश लिखें", "rows": 6}),
        }
