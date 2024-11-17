from django.urls import path
from . import views 

urlpatterns = [
    path('', views.ShowAllEntertainmentView.as_view(), name='all_entertainment'),
    path('profiles', views.ShowAllPeopleView.as_view(), name='users'),
    path('profile/<int:pk>', views.ShowProfilePageView.as_view(), name='person'),
    path('entertainment/<int:pk>', views.ShowEntertainmentPageView.as_view(), name='entertainment'),
]