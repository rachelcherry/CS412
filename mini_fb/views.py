# Rachel Cherry
# rcherry@bu.edu
# views file to render the profiles

from django.shortcuts import render


from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
from .models import *
from django.views.generic import ListView, DetailView #generic view that grabs all the object of that type and send it to a template for rendering


class ShowAllProfilesView(ListView):
    '''A view to show all Profiles'''

    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'
    
class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'
