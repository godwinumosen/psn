from django import forms
from .models import ClearanceApplication

class ClearanceApplicationForm(forms.ModelForm):
    class Meta:
        model = ClearanceApplication
        fields = [
            'membership_number',
            'full_name',
            'technical_group',
            'clearance_year',
            'proof_of_payment',
            'supporting_document',
            'declaration_confirmed',
        ]
        widgets = {
            'technical_group': forms.Select(
                attrs={'class': 'form-select custom-dropdown'}
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)   # 👈 keep your addition
        super().__init__(*args, **kwargs)

        if user:
            # auto-fill membership_number and full_name from logged-in user
            self.fields['membership_number'].initial = user.pcn_number
            self.fields['full_name'].initial = f"{user.first_name} {user.last_name}"

            # make fields readonly so user cannot edit
            self.fields['membership_number'].widget.attrs['readonly'] = True
            self.fields['full_name'].widget.attrs['readonly'] = True

        # ensure the declaration checkbox is required
        self.fields['declaration_confirmed'].required = True
