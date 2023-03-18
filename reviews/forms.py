from django.forms import TextInput, Textarea
from django import forms
from .models import ReviewRating, ReportReview


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']

        widgets = {
            'subject': TextInput(attrs={'class': 'form-control', 'placeholder': 'Give your review a title'}),
            'review': Textarea(attrs={'class': 'form-control h-100', 'placeholder': 'Leave a review'}),
        }

        labels = {
            'subject': "Give your review a title",
            'review': "Leave a review"
        }

    def clean_subject(self):
        subject = self.cleaned_data['subject'].lower()
        if not all(subject.isalnum() or subject.isspace() or subject == ',' or subject == '.'
                   for subject in subject):
            raise forms.ValidationError('This field can only contain letters, numbers, commas and points.')
        return subject

    def clean_review(self):
        review = self.cleaned_data['review'].lower()
        if not all(review.isalnum() or review.isspace() or review in [',', '.', '-', "'", '-', '(', ')']
                   for review in review):
            raise forms.ValidationError('This field can only contain letters, numbers, hyphens, commas, and points.')
        return review


class ReportReviewForm(forms.ModelForm):
    class Meta:
        model = ReportReview
        fields = ['subject', 'description']

        widgets = {
            'subject': TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'description': Textarea(attrs={'class': 'form-control h-100', 'placeholder': 'Description'}),
        }

        labels = {
            'subject': "Subject",
            'description': "Description"
        }

    def clean_subject(self):
        subject = self.cleaned_data['subject'].lower()
        if not all(subject.isalnum() or subject.isspace() or subject == ',' or subject == '.'
                   for subject in subject):
            raise forms.ValidationError('This field can only contain letters, numbers, commas and points.')
        return subject

    def clean_description(self):
        description = self.cleaned_data['description'].lower()
        if not all(description.isalnum() or description.isspace() or description in [',', '.', '-', "'", '-', '(', ')']
                   for description in description):
            raise forms.ValidationError('This field can only contain letters, numbers, hyphens, commas, and points.')
        return description
