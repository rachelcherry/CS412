## hw/urls.py
## description: the app-specofoc URLS for the hr application 

from django.urls import path # path funtion to associate string of url to function that actually does the url
from django.conf import settings
from . import views # 
from django.contrib.auth import views as auth_views ## NEW

#create a list of URLs for this app:

urlpatterns = [
    #path(r'', views.home, name="home"), # give name that matches the function name; This is our first URL; 
    path(r'', views.ShowRandomArticle.as_view(), name="random"),
    path(r'show_all', views.ShowAllView.as_view(), name="show_all"),
    path(r'article/<int:pk>', views.ArticleView.as_view(), name="article"),
    path('article/<int:pk>/create_comment', views.CreateCommentView.as_view(), name='create_comment'), ### NEW
    path(r'create_article', views.CreateArticleView.as_view(), name="create_article"),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page = 'show_all'), name='logout'), 
    path('register/', views.RegistrationView.as_view(), name='register'),

]