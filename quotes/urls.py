## description: the app-specofoc URLS for the hr application 

from django.urls import path # path funtion to associate string of url to function that actually does the url
from django.conf import settings
from . import views # 

#create a list of URLs for this app:

urlpatterns = [
    path(r'', views.quotes, name="quotes"),  # Root URL, matches views.quotes
    path('quotes/', views.quotes, name="quotes"),  # URL for the quote page
    path('about/', views.about, name="about"),  # URL for the about page
    path('show_all/', views.show_all, name="show_all"),  # URL for show_all page
]