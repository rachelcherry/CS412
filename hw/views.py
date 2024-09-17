from django.shortcuts import render

# Create your views here.
# description: the logic to ahndle URL requests 

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random
# def home(request):
#     '''A function to respond to the /hw URL.
#     ''' #doc string

#     #create some text:
#     response_text = f'''
#     <html>
#   <h1>  Hello, world! </h1>
#   <hr>
#   This page was generated at {time.ctime()}.
#     </html>
#     '''

# #return a response to the client 
#     return HttpResponse(response_text)
def home(request):
    '''A function to respond to the /hw URL.
     This function will delegate work to an html template
     ''' 
    #this template will present the response 

    template_name = "hw/home.html"

    #create a dictionary of context variables 
    context = {
        'current_time': time.ctime(),
        'letter1': chr(random.randint(65, 90)), # a letter in the range A to Z
        'letter2': chr(random.randint(65, 90)), # a letter in the range A to Z
        'number1': (random.randint(1, 10)), # a number from 1 to 10

    }
    # delegate response to the template 
    return render(request, template_name, context)
