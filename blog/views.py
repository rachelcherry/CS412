from django.shortcuts import render

# Create your views here.
# description: the logic to ahndle URL requests 

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
from .models import *
from django.views.generic import ListView #generic view that grabs all the object of that type and send it to a template for rendering

class ShowAllView(ListView):
    '''A view to show all Articles'''

    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'
    


