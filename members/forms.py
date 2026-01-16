from django import forms
from .models import User
import re  # ✅ UPDATE (added for phone validation)

# ✅ Use the same name that the form will use
PRACTICE_AREAS = [
    ("Community Pharmacy", "Community Pharmacy"),
    ("Hospital and Administrative Pharmacy", "Hospital and Administrative Pharmacy"),
    ("Industry Pharmacy", "Industry Pharmacy"),
    ("Academia and Research", "Academia and Research"),
    ("Others", "Others"),
]

class RegistrationForm(forms.ModelForm):

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Create a password"
        }),
        required=True
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm your password"
        }),
        required=True
    )

    area_of_practice = forms.ChoiceField(
        label="Area of Practice",
        choices=PRACTICE_AREAS,
        widget=forms.Select(attrs={
            "class": "form-select",
            'style': 'color:#198754; border-color:#198754;'
        }),
        required=True
    )

    workplace_name = forms.CharField(
        label="Current Workplace",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Name of pharmacy/hospital/organization"
        }),
        required=True
    )

    workplace_address = forms.CharField(
        label="Work Address",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Enter workplace address"
        }),
        required=True
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'pcn_number', 'year_qualified',
            'area_of_practice',
            'workplace_name', 'workplace_address',
            'pcn_certificate', 'passport_photo'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter first name"
            }),
            'last_name': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter last name"
            }),
            'email': forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter email"
            }),
            'phone': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+234 xxx xxx xxxx"
            }),
            'pcn_number': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter PCN number"
            }),
            'year_qualified': forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. 2015"
            }),
            'pcn_certificate': forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            'passport_photo': forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Force ALL fields to be compulsory (backend + frontend)
        for field in self.fields.values():
            field.required = True
            field.widget.attrs['required'] = 'required'

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Passwords don't match. Please check and try again."
            )

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Email already been used. Try a new email."
            )

        return email

    # ✅ UPDATE (PHONE VALIDATION ONLY)
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        phone = phone.replace(" ", "")

        pattern = r'^(?:\+234|234|0)(7[0-9]|8[0-9]|9[0-9])[0-9]{8}$'

        if not re.match(pattern, phone):
            raise forms.ValidationError(
                "Enter a valid Nigerian phone number (e.g. 08031234567 or +2348031234567)."
            )

        return phone

    def save(self, commit=True):
        user = super().save(commit=False)

        # set password
        user.set_password(self.cleaned_data["password1"])

        # save area of practice explicitly
        user.area_of_practice = self.cleaned_data.get("area_of_practice")

        if commit:
            user.save()

        return user
