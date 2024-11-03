# Rachel Cherry
# rcherry@bu.edu
# views file to render the profiles

from django.shortcuts import render
from django.contrib.auth import login
# Create your views here.
# description: the logic to ahndle URL requests 
from django.urls import reverse
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.forms import UserCreationForm
import time
from django.views.generic import View
from typing import Any
from .models import *
from django import forms
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView #generic view that grabs all the object of that type and send it to a template for rendering
import random
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
from typing import Any
from .models import *
from django import forms
from django.views.generic.edit import CreateView
from .forms import *
from django.views.generic import ListView, DetailView #generic view that grabs all the object of that type and send it to a template for rendering
import random
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
class ShowAllProfilesView(ListView):
    '''A view to show all Profiles'''

    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'
    
class ShowProfilePageView(DetailView):
    '''A view to show a Profile'''
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        profile = context['profile'] 

        if self.request.user.is_authenticated:
            if self.request.user == profile.user:
                auth_for_profile = True
            else:
                auth_for_profile = False
        else:
            auth_for_profile = None

        context['auth_for_profile'] = auth_for_profile
        return context

    
class CreateProfileView(CreateView):
    '''A view to create a new profile and save it to the database.'''
    form_class = CreateProfileForm 
    template_name = "mini_fb/create_profile_form.html"

    def get_login_url(self) -> str:
        '''Return the URL required for login.'''
        return reverse('login')

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting the form.'''
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['user_creation'] = UserCreationForm() 
        return context

    def form_valid(self, form):
        '''Handle form submission'''
        user_form = UserCreationForm(self.request.POST) 
        if user_form.is_valid():
            user = user_form.save()  
            profile = form.instance 
            profile.user = user 
            profile.save()
            login(self.request, user) 
        return super().form_valid(form)  


class CreateStatusMessageView(CreateView):
        form_class = CreateStatusMessageForm
        template_name = "mini_fb/create_status_form.html"
        ## show how the reverse function uses the urls.py to find the URL pattern
        def get_success_url(self) -> str:
            '''Return the URL to redirect to after successfully submitting form.'''
            profile = Profile.objects.get(user=self.request.user)
            return reverse('profile', kwargs={'pk': profile.pk})
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
            profile = Profile.objects.get(user=self.request.user)
            # print(article)
            # form.instance is the new comment object
            form.instance.profile = profile
            sm = form.save()
            files = self.request.FILES.getlist('files')
            for i in range(len(files)): 
                image_object = Image()
                image_object.image_file = files[i]
                image_object.status_message = sm
                image_object.save()
            return super().form_valid(form)
        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            '''build the template context data -- a dict of key-value pairs'''
            context = super().get_context_data(**kwargs)
            profile = Profile.objects.get(user=self.request.user)
            context['profile'] = profile
            return context
        def get_object(self):
            return Profile.objects.get(user=self.request.user)

class UpdateProfileView(UpdateView):
    '''A view to update a profile'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting form.'''
        return reverse('profile', kwargs={'pk': self.object.pk})
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
class DeleteStatusMessageView(DeleteView):
    '''A view to de;ete a profile'''
    model = StatusMessage
    context_object_name = 'status_message'
    template_name = 'mini_fb/delete_status_form.html'

    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting form.'''
        return reverse('profile', kwargs={'pk': self.object.profile.pk})

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''Build the template context data -- a dict of key-value pairs'''
        context = super().get_context_data(**kwargs)
        status_message = StatusMessage.objects.get(pk=self.kwargs['pk'])
        context['status_message'] = status_message
        context['profile'] = status_message.profile
        return context
class UpdateStatusMessageView(UpdateView):
    '''A view to update a status message'''
    model = StatusMessage
    form_class = UpdateStatusForm
    context_object_name = 'status_message'
    template_name = 'mini_fb/update_status_form.html'

    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting the form.'''
        return reverse('profile', kwargs={'pk': self.object.profile.pk})

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''Build the template context data -- a dict of key-value pairs'''
        context = super().get_context_data(**kwargs)
        status_message = self.object 
        context['profile'] = status_message.profile
        return context
class CreateFriendView(View):
    '''A view to create a friend'''
    def dispatch(self, request, *args, **kwargs):
        profile1 = Profile.objects.get(user=self.request.user)
        profile2 = Profile.objects.get(pk=self.kwargs['other_pk'])
        Profile.add_friend(profile1, profile2)
        return redirect('profile', pk=profile1.pk)
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
class ShowFriendSuggestionsView(DetailView):
    '''A view to show a friend suggestion'''
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
class ShowNewsFeedView(DetailView):
    '''A view to show a news feed'''
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
