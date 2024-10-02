from django.urls import path # path funtion to associate string of url to function that actually does the url
from django.conf import settings
from . import views # 

#create a list of URLs for this app:

urlpatterns = [
    #path(r'', views.home, name="home"), # give name that matches the function name; This is our first URL; 
    path(r'', views.ShowAllProfilesView.as_view(), name="show_all_profiles"),
]