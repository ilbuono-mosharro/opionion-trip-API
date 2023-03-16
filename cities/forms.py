from django import forms
from django.forms import TextInput, Textarea, FileInput, CheckboxInput

from .models import City, ImageCity


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('name', 'title', 'description', 'copertina', 'is_active')

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'description': Textarea(attrs={'class': 'form-control h-100', 'placeholder': 'Description'}),
            'copertina': FileInput(attrs={'class': 'form-control'}),
            'is_active': CheckboxInput(attrs={'class': 'form-check-input'}),

        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if not all(name.isalnum() or name.isspace() for name in name):
            raise forms.ValidationError(
                'This field can only contain letters.')
        return name

    def clean_title(self):
        title = self.cleaned_data['title']
        if not all(title.isalnum() or title.isspace() for title in title):
            raise forms.ValidationError(
                'This field can only contain letters and numbers.')
        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        if not all(description.isalnum() or description.isspace() or description in [',', '.', '-', "'", '-', '(', ')', '"']
                   for description in description):
            raise forms.ValidationError(
                'This field can only contain letters, numbers and ,.-.')
        return description


class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageCity
        fields = ('image', 'alt_text', 'is_active')

        widgets = {
            'alt_text': TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'image': FileInput(attrs={'class': 'form-control'}),
            'is_active': CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_alt_text(self):
        alt_text = self.cleaned_data['alt_text']
        if not all(alt_text.isalpha() or alt_text.isspace() for alt_text in alt_text):
            raise forms.ValidationError(
                'This field can only contain letters.')
        return alt_text
