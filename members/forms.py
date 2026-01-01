from django import forms
from .models import User


PRACTICE_AREAS = [
    ("", "Select practice area"),
    ("community", "Community Pharmacy"),
    ("hospital", "Hospital Pharmacy"),
    ("industry", "Pharmaceutical Industry"),
    ("academia", "Academia"),
    ("regulatory", "Regulatory / Administration"),
    ("ngo", "NGO / Public Health"),
    ("others", "Others"),
]


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Create a password"
        })
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm your password"
        })
    )

    area_of_practice = forms.ChoiceField(
        label="Area of Practice",
        choices=PRACTICE_AREAS,
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )

    workplace_name = forms.CharField(
        label="Current Workplace",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Name of pharmacy/hospital/organization"
        })
    )

    workplace_address = forms.CharField(
        label="Work Address",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Enter workplace address"
        })
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

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Email already been used. Try a new email."
            )

        return email
