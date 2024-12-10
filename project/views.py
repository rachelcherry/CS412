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
class ShowAllEntertainmentView(ListView):
    '''A view to show all peoeple'''
    model = Entertainment # connect it to the Entertainment model
    template_name = 'project/show_all_entertainment.html' # connect to the template
    context_object_name = 'shows' # context variable to use in the template
    paginate_by = 100 # show 100 entertainments per page and use pagination
class ShowProfilePageView(LoginRequiredMixin, DetailView):
    '''A view to show a Profile'''
    model = Person # connect it to the Person model
    template_name = 'project/show_person.html' # connect to the template 
    context_object_name = 'profile' # context variable to use in the template
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''returns context variables for use in the templates'''
        context = super().get_context_data(**kwargs) # use super constructor
        profile = context['profile'] # set profile to be the passed in context variable 'profile'

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
        context['entertainment_list'] = Entertainment.objects.all() # gets all the entertainments
        pers = Person.objects.get(pk=self.kwargs['pk']) # finds the person with this primary key
        context['person'] = pers # set the context variable for this person
        if self.request.user.is_authenticated:
            who = self.request.user.person # find the person who is logged in
            if who == pers or who in pers.get_friends():
                context['yes_friend'] = True
                # if the user matches the current profule or they are friends with the individual logged in, then they have access to the recommendations of another user
                
            else:
                # if they are not friends with the user or do not match the user logged in, they should not be able to see the recommendations button
                context['yes_friend'] = False
        return context
class ShowAllPeopleView(ListView):
    '''A view to show all Profiles'''
    model = Person # connect to the Person model 
    template_name = 'project/show_all_people.html' # connect to the template
    context_object_name = 'profiles' # create a context variable for use in the template

class ShowEntertainmentPageView(DetailView):
    '''A view to show an Entertainment'''
    model = Entertainment # connect to the Entertainment model
    template_name = 'project/show_entertainment.html' # connect to the template
    context_object_name = 'r' # create a context variable for use in the template

class CreateProfileView(CreateView):
    '''A view to create a new profile and save it to the database.'''
    form_class = CreatePersonForm # connect to the form class for creating a new person/profile
    template_name = "project/create_profile_form.html" # connect to the template 

    def get_login_url(self) -> str:
        '''Return the URL required for login.'''
        return reverse('login_url') # use reverse to direct to the login url established in urls.py

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting the form.'''
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs: Any):
        '''returns context variables for use in template'''
        context = super().get_context_data(**kwargs) # call the super class constructor
        context['user_creation'] = UserCreationForm() # use built in UserCreationForm from django to create a new user in the system
        return context 

    def form_valid(self, form):
        '''Handle form submission'''
        user_form = UserCreationForm(self.request.POST) # create a form with the built in UserCreationForm from the POST request
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
    model = Recommendation # connect to the Recommendation model
    form_class = CreateRecommendationForm # connect to the form that creates recommendation
    template_name = "project/create_rec_form.html" # connect to the templates
    def get_context_data(self, **kwargs):
        '''returns context variables for use in templates'''
        context = super().get_context_data(**kwargs) # call the super class constructor 
        context['entertainment_list'] = Entertainment.objects.all() # get all entertainments in the database
        pers= Person.objects.get(pk=self.kwargs['pk']) # get the person associated with the primary key 
        context['person'] = pers  # set the person 
        return context # return all the entertainments
    def form_valid(self, form):
        '''Handle form submission.'''
        profile = Person.objects.get(user=self.request.user) # find the Person object that is linked to the user logged in
        form.instance.person = profile  # set the form instance to be that profile
        ent_pk = self.request.POST.get('entertainment') # find the entertainment that was submitted via the POST request
        ent = Entertainment.objects.get(pk=ent_pk) # find the entertainment associated with the primary key of the entertainment in the POST request
        form.instance.entertainment = ent # set the form instance of entertainment
        sm = form.save()
        files = self.request.FILES.getlist('files')
        print("files", files)
        for i in range(len(files)): 
                image_object = Image()
                image_object.image_file = files[i]
                image_object.recommendation = sm
                image_object.save()
        return super().form_valid(form) # return the super class constructor 

    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting the form.'''
        return reverse('see_recs', kwargs={'pk': self.object.person.pk})

class RecommendationDetailView(DetailView):
    model = Recommendation # connect to Recommendation model
    template_name = 'project/recommendation_detail.html' # connect to template
    context_object_name = 'recommendation' # context data for use in template

class UpdateRecommendationView(LoginRequiredMixin, UpdateView):
    '''A view to update a recommendation. Use LoginRequiredMixin so that only users who are logged in can view this page'''
    model = Recommendation # connect to Recommendation model
    form_class = UpdateRecommendationForm # connect to the form that handles the updating of recommendations
    context_object_name = 'recommendation'
    template_name = 'project/update_rec_form.html'

    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting the form.'''
        return reverse('see_recs', kwargs={'pk': self.object.person.pk})
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''returns the context variables for use in templates'''
        context = super().get_context_data(**kwargs) # call the super class constructor
        context['entertainment_list'] = Entertainment.objects.all() # get all entertainment models
        recommendation = Recommendation.objects.get(pk=self.kwargs['pk']) # get the recommendation associated with the primary key 
        context['person'] = recommendation.person  # set the person of the recommendation 
        return context # return these values so they can be used in the template
class DeleteRecommendationView(LoginRequiredMixin, DeleteView):
    '''A view to delete a profile. Use LoginRequiredMixin so that only users who are logged in can view this page'''
    model = Recommendation # connect to the Recommendation model
    context_object_name = 'recommendation' # context variable for use in the template 
    template_name = 'project/delete_rec_form.html' # connect to template

    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting form.'''
        return reverse('see_recs', kwargs={'pk': self.object.person.pk})

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''returns the context variables for use in the templates'''
        context = super().get_context_data(**kwargs) # call the super class constructor
        context['entertainment_list'] = Entertainment.objects.all() # get all entertainment models
        recommendation = Recommendation.objects.get(pk=self.kwargs['pk']) # get the recommendation associated with the primary key 
        context['person'] = recommendation.person  # set the person of the recommendation 
        return context # return these values so they can be used in the template
class NewsFeedView(LoginRequiredMixin, DetailView):
    '''A view to show the feed with friends' recommendations. Use LoginRequiredMixin so that only users who are logged in can view this page'''
    model = Person # connect to the Person model
    template_name = 'project/news_feed.html' # connect to the template
    context_object_name = 'profile'# context variable for use in the templates
    def get_object(self):
        '''find the user associated with the feed'''
        return Person.objects.get(user=self.request.user)
class ResultsListView(ListView):
    '''View to display list of results from the search query.'''
    template_name = 'project/results.html' # connect to the template
    model = Entertainment # connect to the Entertainment model
    context_object_name = "results" # context variable for use in template
    paginate_by = 100 # show 100 entertainments per page and use pagination 

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''returns context variables for use in templates'''
        context = super().get_context_data(**kwargs) # return the super class constructor
        return context

    def get_queryset(self) -> QuerySet[any]:
        '''returns value of the query set'''
        qs = super().get_queryset() # calls the super class constructor
        if 'title' in self.request.GET: # check if the user searched for title
            title = self.request.GET['title'] # if they did, set the search prompt as the title
            if title: 
                qs = qs.filter(title__icontains=title)  # find the entertainment titles that contain the word(s) in the search
        if 'rating' in self.request.GET: # check if the user searched for rating
            rating = self.request.GET['rating'] # if they did, set the search prompt as the rating
            if rating: 
                qs = qs.filter(rating__icontains=rating)   # find the entertainments that contain the word(s) in the search
        if 'type' in self.request.GET: # check if the user searched for type
            type = self.request.GET['type'] # if they did, set the search prompt as the type
            if type: 
                qs = qs.filter(type=type)  # find the entertainments that contain the word(s) in the search 
        return qs # return the modified list of entertainments
class ResultDetailView(DetailView):
    '''View to show detail page for one result.'''
    template_name = 'project/result_detail.html' # connect to template
    model = Entertainment # connect to Entertainment model
    context_object_name = 'r' # context variable for use in the template
    def get_context_data(self, **kwargs) :
        '''return context variables for use in template'''
        context = super().get_context_data(**kwargs) # call super class constructor
        r = context['r'] # set the context variable for use in the template
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
    template_name = 'project/top_5_month.html'  # connect to the template
    def get_context_data(self, **kwargs):
        '''returns the context variables for use in templates'''
        best5 = top_5() # call  the top_5() function in the models to generate the top 5 list per month
        context = super().get_context_data(**kwargs) # call the super class constructor
        context['top_5'] = best5 # set the context variable to be the results from the top_5 function
        return context # return the context variables for use in the template
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    '''A view to show a friend suggestion. Use LoginRequiredMixin so that only users who are logged in can view this page'''
    model = Person # connect to Person model
    template_name = 'project/friend_suggestions.html' # connect to template 
    context_object_name = 'profile' # context variable for use in template
    def get_object(self):
        ''' finds the Person model who is linked to the user who is logged in'''
        return Person.objects.get(user=self.request.user)
class CreateFriendView(LoginRequiredMixin, View):
    '''A view to create a friend. Use LoginRequiredMixin so that only users who are logged in can view this page'''
    def dispatch(self, request, *args, **kwargs):
        '''establishes friendships between users'''
        profile1 = Person.objects.get(user=self.request.user)  # sets the profile1 to be the logged in user
        profile2 = Person.objects.get(pk=self.kwargs['other_pk']) # sets the profile2 to be the user with the other primary key 
        Person.add_friend(profile1, profile2) # call add_friend method to add the friendship
        return redirect('person', pk=profile1.pk) # call redirect to send the user to the profile page of the logged in user
    def get_object(self):
        '''gets the Person object that matches the logged in user'''
        return Person.objects.get(user=self.request.user)
class SeeRecsView(ListView):
    ''' view to show the recommendations for a particular user'''
    model = Recommendation # connect to the Recommendation model
    template_name = 'project/see_recs.html' # connect to the template
    context_object_name = 'recs' # context variable for use in template

    def get_queryset(self):
        '''find the recommendations that match the user's primary key'''
        return Recommendation.objects.filter(person__pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''return context variables for use in templates'''
        context = super().get_context_data(**kwargs) # call the super class constructor 
        context['entertainment_list'] = Entertainment.objects.all() # gets all the entertainments
        pers = Person.objects.get(pk=self.kwargs['pk']) # finds the person with this primary key
        context['person'] = pers # set the context variable for this person
        who = self.request.user.person # find the person who is logged in
        if who == pers:
            context['yes_person'] = True
            # if the user matches the current profule or they are friends with the individual logged in, then they have access to the recommendations of another user
            
        else:
            # if they are not friends with the user or do not match the user logged in, they should not be able to see the recommendations button
            context['yes_person'] = False
        return context
class UpdateProfView(LoginRequiredMixin, UpdateView):
    '''A view to update a profile'''
    model = Person # connect to Person model
    form_class = UpdateProfileForm # connect to form that handles the updating of profiles
    template_name = 'project/update_profile_form.html' # connect to template

    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting form.'''
        return reverse('person', kwargs={'pk': self.object.pk})
    def get_object(self):
        '''finds the profile if the user who is logged in'''
        return Person.objects.get(user=self.request.user)
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''returns context variables for use in templates'''
        context = super().get_context_data(**kwargs) # calls super class constructor
        context['entertainment_list'] = Entertainment.objects.all() # gets all entertainment objects
        context['person'] = Person.objects.get(pk=self.kwargs['pk']) #gets the person/profile for the Person object whose pk is specified
        return context # return these variables for use in templates
class EntDetailView(DetailView):
    '''View to show detail page for one result of the search query.'''
    model = Entertainment # connect to the Entertainment model
    template_name = 'project/result_detail.html' # connect to the template
    context_object_name = 'r' # create a context variable for use in the template