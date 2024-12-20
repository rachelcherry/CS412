# Rachel Cherry
# rcherry@bu.edu

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    '''A form to create a new Profile.'''
    class Meta:
        '''Associate this form with the Profile model and select fields.'''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'image_url']  # which fields from model should we use
class CreateStatusMessageForm(forms.ModelForm):
        '''A form to create a new Status Message.'''
        class Meta:
            '''Associate this form with the Profile model and select fields.'''
            model = StatusMessage
            fields = ['message'] 
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        '''Associate this form with a Model, specify which fields '''
        model = Profile
        fields = ['city', 'email', 'image_url']
class UpdateStatusForm(forms.ModelForm):
    class Meta:
        '''Associate this form with a Model, specify which fields'''
        model = StatusMessage
        fields = ['message']
