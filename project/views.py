from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
from typing import Any
from .models import *
from django import forms
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView 
import random
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

class ShowAllEntertainmentView(ListView):
    '''A view to show all peoeple'''
    model = Entertainment
    template_name = 'project/show_all_entertainment.html'
    context_object_name = 'shows'
    paginate_by = 100
class ShowProfilePageView(DetailView):
    '''A view to show a Profile'''
    model = Person
    template_name = 'project/show_person.html'
    context_object_name = 'profile'
class ShowAllPeopleView(ListView):
    '''A view to show all Profiles'''
    model = Person
    template_name = 'project/show_all_people.html'
    context_object_name = 'profiles'

class ShowEntertainmentPageView(DetailView):
    '''A view to show a Profile'''
    model = Entertainment
    template_name = 'project/show_entertainment.html'
    context_object_name = 'r'