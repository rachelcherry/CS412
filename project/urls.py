from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views ## NEW

# Rachel Cherry 
# rcherry@bu.edu
# Date created: November 12, 2024
# project/urls.py
# this file handles all url mappings for the application

urlpatterns = [
    # url for the home page
    path('', views.ShowAllEntertainmentView.as_view(), name='all_entertainment'),
    # url for the list of all profiles
    path('profiles', views.ShowAllPeopleView.as_view(), name='users'),
    # url for an individual profile
    path('profile/<int:pk>', views.ShowProfilePageView.as_view(), name='person'),
    # url for a specific entertainment
    path('entertainment/<int:pk>', views.ShowEntertainmentPageView.as_view(), name='entertainment'),
    # url for the creation of a new profile
    path('new_profile', views.CreateProfileView.as_view(), name='new_profile'),
    # url for the creation of a new recommendation
    path('recommendation/create_rec/<int:pk>', views.CreateRecommendationView.as_view(), name='create_rec'),
    # url for the login
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name="login_url"),
    # url for the updating of a recommendation
    path('recommendation/<int:pk>/update', views.UpdateRecommendationView.as_view(), name='update_rec'),
    # url for the deletion of a recommendation
    path('recommendation/<int:pk>/delete', views.DeleteRecommendationView.as_view(), name='delete_rec'),
    # url for the recommendation feed for a user
    path('profile/rec_feed', views.NewsFeedView.as_view(), name='rec_feed'),
    # url for the results from the search query 
    path('entertainment/results/', views.ResultsListView.as_view(), name='searched_list'),
    # url for the top 10 entertainment
    path('entertainment/top10/', views.Top10View.as_view(), name='top_10'),
    # url for the top 5 entertainment per month
    path('entertainment/top5/', views.Top5MonthView.as_view(), name='top_5'),
    # url for logging out users
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name='logout_url'), 
    # url for friend suggestions for a specific user
    path('profile/friend_suggestions', views.ShowFriendSuggestionsView.as_view(), name='new_friends'),
    # url for adding a friend
    path('profile/add_friend/<int:other_pk>', views.CreateFriendView.as_view(), name='add_a_friend'),
    # url for seeing a user's recommendations
    path('profile/<int:pk>/see_rec/', views.SeeRecsView.as_view(), name='see_recs'),
    # url for updating a profile
    path('profile/<int:pk>/update', views.UpdateProfView.as_view(), name='update_prof'),
    # url for viewing an entertainment after searching
    path('entertainment/results/<int:pk>', views.EntDetailView.as_view(), name='ent_detail'),


]