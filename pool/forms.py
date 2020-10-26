from django import forms
from django.core.exceptions import ValidationError

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class UploadTargetForm(forms.Form):
    categories = (
        ('PERSON', 'Person'),
        ('LIFEFORM', 'Lifeform'),
        ('OBJECT', 'Object'),
        ('LOCATION', 'Location'),
        ('EVENT', 'Event'),
        ('OTHER', 'Other')
    )
    category = forms.ChoiceField(choices=categories)
    additional_feedback = forms.CharField(widget=forms.Textarea(), required=False)
    tasking = forms.CharField(widget=forms.Textarea())
    target_description = forms.CharField(max_length=255)
    feedback_image = forms.ImageField()
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

class GetTargetForm(forms.Form):
    person = forms.BooleanField(required=False)
    lifeform = forms.BooleanField(required=False)
    object = forms.BooleanField(required=False)
    location = forms.BooleanField(required=False)
    event = forms.BooleanField(required=False)
    other = forms.BooleanField(required=False)
    precognitive = forms.BooleanField(required=False)
    incsubmitted = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super().clean()

        categories = ['person', 'lifeform', 'object',
                      'location', 'event', 'other']
        selected_categories = list()
        for category in categories:
            if cleaned_data.get(category):
                selected_categories.append(category.upper())

        if not selected_categories:
            raise ValidationError('You need to select at least one category.')

        cleaned_data['selected_categories'] = selected_categories
        return cleaned_data

class NewPersonalTargetForm(forms.Form):
    tasking = forms.CharField(widget=forms.Textarea(), required=True)