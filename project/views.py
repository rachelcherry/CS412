from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
from django.db.models.query import QuerySet
from typing import Any
from django.shortcuts import redirect

from .models import *
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, TemplateView, View
import random
from django.contrib.auth import login
from django.urls import reverse
from .forms import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm

# Rachel Cherry 
# rcherry@bu.edu
# Date created: November 12, 2024
# project/urls.py
# this file handles all views for the application

class ShowAllEntertainmentView(ListView):
    '''A view to show all peoeple'''
    # connect it to the Entertainment model
    model = Entertainment 
     # connect to the template
    template_name = 'project/show_all_entertainment.html'
    # context variable to use in the template
    context_object_name = 'shows' 
     # show 100 entertainments per page and use pagination
    paginate_by = 100
class ShowProfilePageView(LoginRequiredMixin, DetailView):
    '''A view to show a Profile'''
    # connect it to the Person model
    model = Person 
    # connect to the template 
    template_name = 'project/show_person.html' 
    # context variable to use in the template
    context_object_name = 'profile' 

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''returns context variables for use in the templates'''
         # use super constructor
        context = super().get_context_data(**kwargs)
         # set profile to be the passed in context variable 'profile'
        profile = context['profile']

        # check if the user is logged in
        if self.request.user.is_authenticated:
            # check if the logged in user matches the user of the current profile logged in
            if self.request.user == profile.user:
                # set this context variable to true if they match the profile
                auth_for_profile = True
            else:
                # otherwise it is set to false
                auth_for_profile = False
        else:
            # if the user is not authenticated (i.e. not logged in) set the value to None
            auth_for_profile = None
        # set the context variable for this boolean and return the context for use in the templates
        context['auth_for_profile'] = auth_for_profile 
        # gets all the entertainments
        context['entertainment_list'] = Entertainment.objects.all() 
        # finds the person with this primary key
        pers = Person.objects.get(pk=self.kwargs['pk']) 
        # set the context variable for this person
        context['person'] = pers 
        if self.request.user.is_authenticated:
            # find the person who is logged in
            who = self.request.user.person 
            # if the person is the one logged in or friends with the user logged in
            if who == pers or who in pers.get_friends():
                  # if the user matches the current profule or they are friends with the individual logged in, then they have access to the recommendations of another user
                context['yes_friend'] = True
              
            else:
                # if they are not friends with the user or do not match the user logged in, they should not be able to see the recommendations button
                context['yes_friend'] = False
        return context
class ShowAllPeopleView(ListView):
    '''A view to show all Profiles'''
    # connect to the Person model 
    model = Person 
    # connect to the template
    template_name = 'project/show_all_people.html' 
     # create a context variable for use in the template
    context_object_name = 'profiles'

class ShowEntertainmentPageView(DetailView):
    '''A view to show an Entertainment'''
    # connect to the Entertainment model
    model = Entertainment 
     # connect to the template
    template_name = 'project/show_entertainment.html'
    # create a context variable for use in the template
    context_object_name = 'r' 

class CreateProfileView(CreateView):
    '''A view to create a new profile and save it to the database.'''
    # connect to the form class for creating a new person/profile
    form_class = CreatePersonForm 
    # connect to the template 
    template_name = "project/create_profile_form.html" 

    def get_login_url(self) -> str:
        '''Return the URL required for login.'''
        # use reverse to direct to the login url established in urls.py
        return reverse('login_url') 

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting the form.'''
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs: Any):
        '''returns context variables for use in template'''
        # call the super class constructor
        context = super().get_context_data(**kwargs) 
         # use built in UserCreationForm from django to create a new user in the system
        context['user_creation'] = UserCreationForm()
        return context 

    def form_valid(self, form):
        '''Handle form submission'''
        # create a form with the built in UserCreationForm from the POST request
        user_form = UserCreationForm(self.request.POST) 
        if user_form.is_valid():
            # if the form is valid then save it to the database
            user = user_form.save()  
            # set the profile to be the instance of the form
            profile = form.instance 
            # assign the profile's user to be the user from the user creation form
            profile.user = user 
            # save the profile to the database
            profile.save()
            # login the user after they have created their profile with the new user account
            login(self.request, user) 
            # return the super constructor
            return super().form_valid(form)  
        else:
            # if the form is not valid return form_invalid
            return super().form_invalid(form)
class CreateRecommendationView(LoginRequiredMixin, CreateView):
    '''a view to create a new recommendation. Use LoginRequiredMixin so that only users who are logged in can view this page'''
    # connect to the Recommendation model
    model = Recommendation 
    # connect to the form that creates recommendation
    form_class = CreateRecommendationForm 
    # connect to the templates
    template_name = "project/create_rec_form.html" 
    def get_context_data(self, **kwargs):
        '''returns context variables for use in templates'''
        # call the super class constructor 
        context = super().get_context_data(**kwargs) 
        # get all entertainments in the database
        context['entertainment_list'] = Entertainment.objects.all() 
        # get the person associated with the primary key 
        pers= Person.objects.get(pk=self.kwargs['pk']) 
         # set the person 
        context['person'] = pers 
        # return all the entertainments
        return context 
    def form_valid(self, form):
        '''Handle form submission.'''
        # find the Person object that is linked to the user logged in
        profile = Person.objects.get(user=self.request.user) 
        # set the form instance to be that profile
        form.instance.person = profile  
        # find the entertainment that was submitted via the POST request
        ent_pk = self.request.POST.get('entertainment') 
        # find the entertainment associated with the primary key of the entertainment in the POST request
        ent = Entertainment.objects.get(pk=ent_pk) 
        # set the form instance of entertainment
        form.instance.entertainment = ent 
        sm = form.save()
        files = self.request.FILES.getlist('files')
        print("files", files)
        # loop through the files chosen
        for i in range(len(files)): 
                image_object = Image()
                # set the files
                image_object.image_file = files[i]
                image_object.recommendation = sm
                # save the files as part of the recommendation 
                image_object.save()
        # return the super class constructor 
        return super().form_valid(form) 

    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting the form.'''
        return reverse('see_recs', kwargs={'pk': self.object.person.pk})

class RecommendationDetailView(DetailView):
    # connect to Recommendation model
    model = Recommendation 
    # connect to template
    template_name = 'project/recommendation_detail.html' 
     # context data for use in template
    context_object_name = 'recommendation'

class UpdateRecommendationView(LoginRequiredMixin, UpdateView):
    '''A view to update a recommendation. Use LoginRequiredMixin so that only users who are logged in can view this page'''
    # connect to Recommendation model
    model = Recommendation 
     # connect to the form that handles the updating of recommendations
    form_class = UpdateRecommendationForm
    context_object_name = 'recommendation'
    template_name = 'project/update_rec_form.html'

    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting the form.'''
        return reverse('see_recs', kwargs={'pk': self.object.person.pk})
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''returns the context variables for use in templates'''
         # call the super class constructor
        context = super().get_context_data(**kwargs)
         # get all entertainment models
        context['entertainment_list'] = Entertainment.objects.all()
        # get the recommendation associated with the primary key 
        recommendation = Recommendation.objects.get(pk=self.kwargs['pk']) 
         # set the person of the recommendation 
        context['person'] = recommendation.person 
        # return these values so they can be used in the template
        return context 
class DeleteRecommendationView(LoginRequiredMixin, DeleteView):
    '''A view to delete a profile. Use LoginRequiredMixin so that only users who are logged in can view this page'''
    # connect to the Recommendation model
    model = Recommendation 
    # context variable for use in the template 
    context_object_name = 'recommendation' 
    # connect to template
    template_name = 'project/delete_rec_form.html' 

    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting form.'''
        return reverse('see_recs', kwargs={'pk': self.object.person.pk})

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''returns the context variables for use in the templates'''
        # call the super class constructor
        context = super().get_context_data(**kwargs) 
        # get all entertainment models
        context['entertainment_list'] = Entertainment.objects.all() 
         # get the recommendation associated with the primary key 
        recommendation = Recommendation.objects.get(pk=self.kwargs['pk'])
         # set the person of the recommendation 
        context['person'] = recommendation.person 
        # return these values so they can be used in the template
        return context 
class NewsFeedView(LoginRequiredMixin, DetailView):
    '''A view to show the feed with friends' recommendations. Use LoginRequiredMixin so that only users who are logged in can view this page'''
    # connect to the Person model
    model = Person 
     # connect to the template
    template_name = 'project/news_feed.html'
    context_object_name = 'profile'
    def get_object(self):
        '''find the user associated with the feed'''
        return Person.objects.get(user=self.request.user)
class ResultsListView(ListView):
    '''View to display list of results from the search query.'''
     # connect to the template
    template_name = 'project/results.html'
    # connect to the Entertainment model
    model = Entertainment 
    # context variable for use in template
    context_object_name = "results" 
    # show 100 entertainments per page and use pagination 
    paginate_by = 100 

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''returns context variables for use in templates'''
        # return the super class constructor
        context = super().get_context_data(**kwargs) 
        return context

    def get_queryset(self) -> QuerySet[any]:
        '''returns value of the query set'''
         # calls the super class constructor
        qs = super().get_queryset()
        # check if the user searched for title
        if 'title' in self.request.GET: 
            # if they did, set the search prompt as the title
            title = self.request.GET['title'] 
            if title: 
                # find the entertainment titles that contain the word(s) in the search
                qs = qs.filter(title__icontains=title)  
                # check if the user searched for rating
        if 'rating' in self.request.GET: 
             # if they did, set the search prompt as the rating
            rating = self.request.GET['rating']
            if rating: 
                 # find the entertainments that contain the word(s) in the search
                qs = qs.filter(rating__icontains=rating)  
        # check if the user searched for type
        if 'type' in self.request.GET: 
            # if they did, set the search prompt as the type
            type = self.request.GET['type'] 
            if type: 
                 # find the entertainments that contain the word(s) in the search 
                qs = qs.filter(type=type) 
        # return the modified list of entertainments
        return qs 
class ResultDetailView(DetailView):
    '''View to show detail page for one result.'''
     # connect to template
    template_name = 'project/result_detail.html'
    # connect to Entertainment model
    model = Entertainment 
    # context variable for use in the template
    context_object_name = 'r' 
    def get_context_data(self, **kwargs) :
        '''return context variables for use in template'''
        # call super class constructor
        context = super().get_context_data(**kwargs) 
        # set the context variable for use in the template
        r = context['r'] 
        return context

class Top10View(TemplateView):
    '''view to show the top 10 rated entertainments'''
    # connect to the template
    template_name = 'project/top_10.html'  
    def get_context_data(self, **kwargs):
        '''return context variables for use in the templates '''
        # call the top_10 function in the models to generate the top 10 list 
        best = top_10() 
        # call the super class constructor 
        context = super().get_context_data(**kwargs) 
        # set the context variable to be the results from the top_10 function
        context['top_10'] = best 
        # return the context variables for use in the template
        return context 
class Top10View(TemplateView):
    '''view to show the top 10 rated entertainments'''
    template_name = 'project/top_10.html'  # connect to the template
    def get_context_data(self, **kwargs):
        '''return context variables for use in the templates '''
        best = top_10() # call the top_10 function in the models to generate the top 10 list 
        context = super().get_context_data(**kwargs) # call the super class constructor 
        context['top_10'] = best # set the context variable to be the results from the top_10 function
        return context # return the context variables for use in the template
class Top5MonthView(TemplateView):
    '''view to show the top 5 rated entertainments per month'''
     # connect to the template
    template_name = 'project/top_5_month.html' 
    def get_context_data(self, **kwargs):
        '''returns the context variables for use in templates'''
        # call  the top_5() function in the models to generate the top 5 list per month
        best5 = top_5() 
         # call the super class constructor
        context = super().get_context_data(**kwargs)
        # set the context variable to be the results from the top_5 function
        context['top_5'] = best5 
        # return the context variables for use in the template
        return context 
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    '''A view to show a friend suggestion. Use LoginRequiredMixin so that only users who are logged in can view this page'''
    # connect to Person model
    model = Person 
    # connect to template 
    template_name = 'project/friend_suggestions.html' 
     # context variable for use in template
    context_object_name = 'profile'
    def get_object(self):
        ''' finds the Person model who is linked to the user who is logged in'''
        return Person.objects.get(user=self.request.user)
class CreateFriendView(LoginRequiredMixin, View):
    '''A view to create a friend. Use LoginRequiredMixin so that only users who are logged in can view this page'''
    def dispatch(self, request, *args, **kwargs):
        '''establishes friendships between users'''
         # sets the profile1 to be the logged in user
        profile1 = Person.objects.get(user=self.request.user) 
        # sets the profile2 to be the user with the other primary key 
        profile2 = Person.objects.get(pk=self.kwargs['other_pk']) 
        # call add_friend method to add the friendship
        Person.add_friend(profile1, profile2) 
        # call redirect to send the user to the profile page of the logged in user
        return redirect('person', pk=profile1.pk) 
    def get_object(self):
        '''gets the Person object that matches the logged in user'''
        return Person.objects.get(user=self.request.user)
class SeeRecsView(ListView):
    ''' view to show the recommendations for a particular user'''
    # connect to the Recommendation model
    model = Recommendation 
     # connect to the template
    template_name = 'project/see_recs.html'
     # context variable for use in template
    context_object_name = 'recs'

    def get_queryset(self):
        '''find the recommendations that match the user's primary key'''
        return Recommendation.objects.filter(person__pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''return context variables for use in templates'''
        # call the super class constructor 
        context = super().get_context_data(**kwargs) 
        # gets all the entertainments
        context['entertainment_list'] = Entertainment.objects.all() 
        # finds the person with this primary key
        pers = Person.objects.get(pk=self.kwargs['pk']) 
        # set the context variable for this person
        context['person'] = pers 
        # check if the user is authenticated
        if self.request.user.is_authenticated:
            who = self.request.user.person # find the person who is logged in
            if who == pers:
                # if the user matches the current profile, they should have access to see their own recommendation

                context['yes_person'] = True
                
            else:
                # if they are not friends with the user or do not match the user logged in, they should not be able to see the recommendations button
                context['yes_person'] = False
        return context
class UpdateProfView(LoginRequiredMixin, UpdateView):
    '''A view to update a profile'''
    # connect to Person model
    model = Person 
    # connect to form that handles the updating of profiles
    form_class = UpdateProfileForm 
     # connect to template
    template_name = 'project/update_profile_form.html'

    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting form.'''
        return reverse('person', kwargs={'pk': self.object.pk})
    def get_object(self):
        '''finds the profile if the user who is logged in'''
        return Person.objects.get(user=self.request.user)
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''returns context variables for use in templates'''
        # calls super class constructor
        context = super().get_context_data(**kwargs) 
        # gets all entertainment objects
        context['entertainment_list'] = Entertainment.objects.all() 
        #gets the person/profile for the Person object whose pk is specified
        context['person'] = Person.objects.get(pk=self.kwargs['pk']) 
        # return these variables for use in templates
        return context 
class EntDetailView(DetailView):
    '''View to show detail page for one result of the search query.'''
    # connect to the Entertainment model
    model = Entertainment 
    # connect to the template
    template_name = 'project/result_detail.html' 
    # create a context variable for use in the template
    context_object_name = 'r' 