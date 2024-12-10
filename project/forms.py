# Rachel Cherry
# rcherry@bu.edu
# project/forms.py
# Date created: November 12, 2024
# this file handles all of the forms within the application 

from django import forms
from .models import Person, Recommendation

# This form will handle the creation of a new Person / profile in the application
class CreatePersonForm(forms.ModelForm):
    '''A form to create a new Profile.'''
    class Meta:
        '''Associate this form with the Person model and select fields.'''
        # connect to Person model 
        model = Person 
        # fields that the user can use to create a new profile
        fields = ['first_name', 'last_name', 'address', 'email', 'dob', 'image_url'] 

# This form will handle the creation of a new recommendation in the application
class CreateRecommendationForm(forms.ModelForm):
        '''A form to create a new Recommendation'''
        class Meta:
            '''Associate this form with the Profile model and select fields.'''
             # connect to the Recommendation model
            model = Recommendation
             # fields that the user can use to create a new recommendation
            fields = ['thoughts', 'rating', 'recommend']

# This form will handle the update of a profile
class UpdateProfileForm(forms.ModelForm):
    '''A form to update an existing profile'''
    class Meta:
        '''Associate this form with the Person model, specify which fields '''
        # connect to the Person model
        model = Person 
        # fields that the user can edit when updating a profile
        fields = ['address', 'email', 'image_url'] 

# This form will Update a recommendation
class UpdateRecommendationForm(forms.ModelForm):
    '''Associate this form with the Recommendation model, specify which fields '''
   
    class Meta:
        '''Associate this form with the Recommendation model, specify which fields'''
        # connect to the Recommendation model
        model = Recommendation 
        # fields that the user can edit when updating a recommendation
        fields = ['thoughts', 'rating'] 
