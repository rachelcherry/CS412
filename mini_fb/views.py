# Rachel Cherry
# rcherry@bu.edu
# views file to render the profiles

from django.shortcuts import render

# Create your views here.
# description: the logic to ahndle URL requests 
from django.urls import reverse

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
from typing import Any
from .models import *
from django import forms
from django.views.generic.edit import CreateView
from .form import *
from django.views.generic import ListView, DetailView #generic view that grabs all the object of that type and send it to a template for rendering
import random
from django.views.generic import ListView, DetailView, CreateView


from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
from typing import Any
from .models import *
from django import forms
from django.views.generic.edit import CreateView
from .form import *
from django.views.generic import ListView, DetailView #generic view that grabs all the object of that type and send it to a template for rendering
import random
from django.views.generic import ListView, DetailView, CreateView
class ShowAllProfilesView(ListView):
    '''A view to show all Profiles'''

    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'
    
class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'


class CreateProfileView(CreateView):
    '''A view to create a new profile and save it to the database.'''
    form_class = CreateProfileForm 
    template_name = "mini_fb/create_profile_form.html"
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        return self.object.get_absolute_url()

class CreateStatusMessageView(CreateView):
        form_class = CreateStatusMessageForm
        template_name = "mini_fb/create_status_form.html"
        ## show how the reverse function uses the urls.py to find the URL pattern
        def get_success_url(self) -> str:
            '''Return the URL to redirect to after successfully submitting form.'''
            return reverse('profile', kwargs=self.kwargs)
            ## note: this is not ideal, because we are redirected to the main page.
        def form_valid(self, form):
            '''
            Handle the form submission. We need to set the foreign key by 
            attaching the Profile to the Comment object.
            We can find the profile PK in the URL (self.kwargs).
            '''
            print(f'CreateStatusMessageView.form.valid(): form={form.cleaned_data}')
            print(f'CreateStatusMessageView.form_valid(): self.kwargs={self.kwargs}')
            # find the article with the PK from the url 
            profile = Profile.objects.get(pk=self.kwargs['pk'])
            # print(article)
            # form.instance is the new comment object
            form.instance.profile = profile
            return super().form_valid(form)
        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            '''build the template context data -- a dict of key-value pairs'''

            # get the super class version of context data
            context = super().get_context_data(**kwargs)
            # add the article to the context data 

            profile = Profile.objects.get(pk=self.kwargs['pk'])

            context['profile'] = profile
            return context