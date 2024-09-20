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
    '/static/michelle3.jpg'

    
    ]
# Create your views here.
def quotes(request):
    template_name = "quotes/quotes.html"
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

    #create some text:
    context = {
        'current_time': time.ctime(),
        'michelle_img1': 'https://www.google.com/url?sa=i&url=https%3A%2F%2Ffortune.com%2Fwell%2F2023%2F05%2F03%2Fmichelle-obama-new-food-beverage-brand-plezi-healthy-children-obesity%2F&psig=AOvVaw2VV2fTa3B6AyeQzOXvm6LG&ust=1726799075635000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCPCZ1_35zYgDFQAAAAAdAAAAABAJ', 
        'michelle_img2': 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FMichelle_Obama&psig=AOvVaw096XNT7BjsnA9fVU49JJOj&ust=1726799482058000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCOizmb_7zYgDFQAAAAAdAAAAABAJ',
        'michelle_img3': 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.harpersbazaar.com%2Ffashion%2Ftrends%2Fg813%2Fmichelle-obama-fashion%2F&psig=AOvVaw096XNT7BjsnA9fVU49JJOj&ust=1726799482058000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCOizmb_7zYgDFQAAAAAdAAAAABAa',
        'michelle_img4': 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.harpersbazaar.com%2Ffashion%2Ftrends%2Fg813%2Fmichelle-obama-fashion%2F&psig=AOvVaw096XNT7BjsnA9fVU49JJOj&ust=1726799482058000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCOizmb_7zYgDFQAAAAAdAAAAABAs',
        'michelle_quote1': 'Success is only meaningful and enjoyable if it feels like your own.', 
        'michelle_quote2': 'Instead of letting your hardships and failures discourage or exhaust you, let them inspire you.', 
        'michelle_quote3': 'Lead by example with hope, never fear.', 
        'michelle_quote4': 'If you don’t get out there and define yourself, you’ll be quickly and inaccurately defined by others.'
    }
    return render(request, template_name, context)
