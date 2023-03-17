from django import forms
from django.forms import TextInput, Textarea, FileInput, CheckboxInput, Select, NumberInput
from cities.models import City
from .models import Attractions, ImageAttractions


class AttractionsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.cities.cities_active()

    class Meta:
        model = Attractions
        fields = ('city', 'name', 'adress', 'cap', 'title', 'description', 'copertina', 'is_active')

        widgets = {
            'city': Select(attrs={'class': 'form-select', 'placeholder': 'Select a City'}),
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'adress': TextInput(attrs={'class': 'form-control', 'placeholder': 'Adress'}),
            'cap': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cap'}),
            'description': Textarea(attrs={'class': 'form-control h-100', 'placeholder': 'Description'}),
            'copertina': FileInput(attrs={'class': 'form-control'}),
            'is_active': CheckboxInput(attrs={'class': 'form-check-input'}),

        }
        labels = {
            'city': 'Select a City',
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
                'This field can only contain letters.')
        return title

    def clean_adress(self):
        adress = self.cleaned_data['adress']
        if not all(adress.isalnum() or adress.isspace() or adress == ',' or adress == '.' or
                   adress == '-' for adress in adress):
            raise forms.ValidationError(
                'This field can only contain letters, numbers and ,.-.')
        return adress

    def clean_description(self):
        description = self.cleaned_data['description']
        if not all(
                description.isalnum() or description.isspace()
                or description in [',', '.', '-', "'", '-', '(', ')', '"', '!', '/', '?'] for description in description
        ):
            raise forms.ValidationError(
                'This field can only contain letters, numbers and ,.-.')
        return description


class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageAttractions
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
