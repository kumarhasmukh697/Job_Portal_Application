from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Application, Job, User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.Role.choices)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "role")


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ("title", "company", "description", "salary", "location", "category", "is_active")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 6}),
            "salary": forms.NumberInput(attrs={"min": "0", "step": "0.01"}),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ("cover_letter",)
        widgets = {
            "cover_letter": forms.Textarea(
                attrs={"rows": 5, "placeholder": "Tell the employer why you are a good fit."}
            )
        }


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ("status",)
