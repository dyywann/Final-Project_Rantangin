from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class UserRegistrationForm(UserCreationForm):
    name = forms.CharField(required=True)
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    GENDER = [
        (MALE, "Male"),
        (FEMALE, "Female"),
    ]
    gender = forms.TypedChoiceField(
        widget=forms.RadioSelect(attrs={'class': 'form-check-label'}),
        choices=GENDER,
        initial=MALE,
        coerce=str,
    )

    class Meta:
        model = User
        fields = ['name', 'email', 'username', 'password1', 'password2', 'gender']



class CheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Rawamangun 1234 Main St'
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    same_billing_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)