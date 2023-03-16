from django import forms
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.forms import Select, TextInput, NumberInput, FileInput
from .models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.core.exceptions import ValidationError

from .token import token_generator


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Repeat Password'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['age'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Age'})
        self.fields['terms_and_privacy'].widget.attrs.update({'class': 'form-check-input'})

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'age', 'terms_and_privacy']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('That username is already taken.')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password_mismatch.')
        return password2

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not all(first_name.isalpha() or first_name.isspace() for first_name in first_name):
            raise forms.ValidationError('This field can only contain letters.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not all(last_name.isalpha() or last_name.isspace() for last_name in last_name):
            raise forms.ValidationError('This field can only contain letters.')
        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This email address is already registered.')
        return email

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age < 18:
            raise forms.ValidationError("You must be at least 18 years old to register.")
        else:
            if age > 99:
                raise forms.ValidationError("Check that you have entered your age correctly.")
        return age

    def send_activation_email(self, request, user):
        current_site = get_current_site(request)
        subject = 'Activate Your Account'
        message = render_to_string(
            'accounts/email_activation.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user),
            }
        )

        user.email_user(subject, message, html_message=message)


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("There is no guest registered with the specified email address!")
        return email


class ModifyProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'age', 'gender', 'city', 'contry', 'avatar')
        widgets = {'first_name': TextInput(attrs={'class': 'form-control'}),
                   'last_name': TextInput(attrs={'class': 'form-control'}),
                   'age': NumberInput(attrs={'class': 'form-control'}),
                   'gender': Select(attrs={'class': 'form-select'}),
                   'city': TextInput(attrs={'class': 'form-control'}),
                   'contry': Select(attrs={'class': 'form-control'}),
                   'avatar': FileInput(attrs={'class': 'form-control', 'accept': '.jpg, .jpeg, .png'}),
                   }

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not all(first_name.isalpha() or first_name.isspace() for first_name in first_name):
            raise forms.ValidationError(
                'This field can only contain letters.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not all(last_name.isalpha() or last_name.isspace() for last_name in last_name):
            raise forms.ValidationError(
                'This field can only contain letters.')
        return last_name

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age < 18:
            raise forms.ValidationError("You must be at least 18 years old to register.")
        else:
            if age > 99:
                raise forms.ValidationError("Check that you have entered your age correctly.")
        return age
