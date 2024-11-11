from django import forms
from .models import Comment, Article

class CreateCommentForm(forms.ModelForm):
    '''A form to add a Comment to the database.'''
    class Meta:
        '''associate this form with the Comment model; select fields.'''
        model = Comment
        fields = ['article', 'author', 'text', ]  # which fields from model should we use
class CreateArticleForm(forms.ModelForm):
    '''A form to create a new article'''

    class Meta:
        '''Associate this form with a Model, specify which fields to create'''
        model = Article
        fields = ['author', 'title', 'text', 'image_file']
        