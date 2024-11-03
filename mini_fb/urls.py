# Rachel Cherry
# rcherry@bu.edu

from django.urls import path # path funtion to associate string of url to function that actually does the url
from django.conf import settings
from . import views # 
from django.contrib.auth import views as auth_views ## NEW
#create a list of URLs for this app:

urlpatterns = [
    path(r'', views.ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path(r'profile/<int:pk>', views.ShowProfilePageView.as_view(), name='profile'),
    path(r'create_profile', views.CreateProfileView.as_view(), name='create_profile'),
    path(r'profile/create_status', views.CreateStatusMessageView.as_view(), name='create_status'),
    path(r'profile/update', views.UpdateProfileView.as_view(), name='update_profile'),
    path(r'status/<int:pk>/delete', views.DeleteStatusMessageView.as_view(), name='delete_status'),
    path(r'status/<int:pk>/update', views.UpdateStatusMessageView.as_view(), name='update_status'),
    path(r'profile/add_friend/<int:other_pk>', views.CreateFriendView.as_view(), name='add_friend'),
    path(r'profile/friend_suggestions', views.ShowFriendSuggestionsView.as_view(), name='friend_suggestion'),
    path(r'profile/news_feed', views.ShowNewsFeedView.as_view(), name='news_feed'),
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'), 

]
