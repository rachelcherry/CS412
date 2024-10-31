from django.shortcuts import render

# Create your views here.
# description: the logic to ahndle URL requests 

from django.shortcuts import render, redirect
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login




class ShowAllView(ListView):
    '''A view to show all Articles'''

    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'

    def dispatch(self, *args, **kwargs):
        '''implement this method to add some tracing'''
        # delegate to superclass version 
        print(f"self.request.user={self.request.user}")
        return super().dispatch(*args, *kwargs)
    
## implement the get_object method 
class ShowRandomArticle(DetailView):
    '''Show one article selected at random.'''
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'
    def get_object(self):
        '''Return the instance of the Article object to show'''
        all_articles = Article.objects.all() # SELECT *
        return random.choice(all_articles)
class ArticleView(DetailView):
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'

from django.urls import reverse
class CreateCommentView(CreateView):
    '''A view to create a new comment and save it to the database.'''
    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"
    ## show how the reverse function uses the urls.py to find the URL pattern
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        return reverse('article', kwargs=self.kwargs)
        ## note: this is not ideal, because we are redirected to the main page.
    def form_valid(self, form):
        '''
        Handle the form submission. We need to set the foreign key by 
        attaching the Article to the Comment object.
        We can find the article PK in the URL (self.kwargs).
        '''
        print(f'CreateCommentView.form.valid(): form={form.cleaned_data}')
        print(f'CreateCommentView.form_valid(): self.kwargs={self.kwargs}')
        # find the article with the PK from the url 
        article = Article.objects.get(pk=self.kwargs['pk'])
        # print(article)
        # form.instance is the new comment object
        form.instance.article = article
        return super().form_valid(form)
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''build the template context data -- a dict of key-value pairs'''

        # get the super class version of context data
        context = super().get_context_data(**kwargs)


        # add the article to the context data 

        article = Article.objects.get(pk=self.kwargs['pk'])

        context['article'] = article
        return context
class CreateArticleView(LoginRequiredMixin, CreateView):
    '''A view to create a new Article instance'''
    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def form_valid(self, form):
        '''Add some debugging statements.'''
        print(f'CreateArticleViewf.form_valid: {form.cleaned_data}')
        # find the user that is logged in 
        user = self.request.user
        print(f'CreateArticleView:form_valid() user{user}' )
        # attach the user to the new article instance 
        form.instance.user = user
        # delegate work to superclass
        return super().form_valid(form)

class RegistrationView(CreateView):
    '''display and process the UserCreationForm for account registration'''
    template_name = 'blog/register.html'
    form_class = UserCreationForm

    def dispatch(self, *args, **kwargs):
        '''handle the User creation process.'''
        ## we handle the POST request:
        if self.request.POST:
            #reconstruct UserCreationForm from the HTTP POST
            print(f"self.request.POST={self.request.POST}")
           

            form = UserCreationForm(self.request.POST)
            print(form)
            
            if not form.is_valid():
                print(f"form errors: {form.errors}")
                return super().dispatch(*args, **kwargs)

            # attach user to profile creation form before saving in mini_fb

            #save the user object
            user = form.save() # creates a new instance of a User object in the database 
            print(f"self.request.user={user}")
            
            #log in the User

            login(self.request, user) 

            # redirect the user to some page view 

            return  redirect(reverse('show_all'))
        # let default superclass CreateView handle the http GET request"
        return super().dispatch(*args, **kwargs)