# Rachel Cherry
# rcherry@bu.edu

from django.urls import path # path funtion to associate string of url to function that actually does the url
from django.conf import settings
from . import views # 

#create a list of URLs for this app:

urlpatterns = [
    path(r'', views.ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path(r'profile/<int:pk>', views.ShowProfilePageView.as_view(), name="profile"),
]