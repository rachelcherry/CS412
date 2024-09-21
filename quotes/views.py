from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random
quote_list = [
        'Success is only meaningful and enjoyable if it feels like your own.', 
        'Instead of letting your hardships and failures discourage or exhaust you, let them inspire you.', 
        'Lead by example with hope, never fear.',
        'If you don’t get out there and define yourself, you’ll be quickly and inaccurately defined by others.'
    ]
photo_list = [
    '/static/michelle.jpg',
    '/static/michelle2.jpg',
    '/static/michelle3.webp',
    ]
# Create your views here.
def quotes(request):
    template_name = "quotes/quote.html"
    # '''A function to respond to the /quotes URL.
    # ''' #doc string

    # #create some text:
    context = {
        'current_time': time.ctime(),
        'michelle_img': random.choice(photo_list),
        'michelle_quote': random.choice(quote_list),

    }
    return render(request, template_name, context)

def about(request):
    template_name = "quotes/about.html"
    return render(request, template_name)

def show_all(request):
    template_name = "quotes/show_all.html"
    '''A function to respond to the /quotes URL.
    ''' #doc string


    context = {
        'current_time': time.ctime(),
        'michelle_imgs': [ '/static/michelle.jpg','/static/michelle2.jpg','/static/michelle3.webp'],
        'michelle_quotes': ['Success is only meaningful and enjoyable if it feels like your own.', 'Instead of letting your hardships and failures discourage or exhaust you, let them inspire you.', 'Lead by example with hope, never fear.', 'If you don’t get out there and define yourself, you’ll be quickly and inaccurately defined by others.'],
    }
    return render(request, template_name, context)
