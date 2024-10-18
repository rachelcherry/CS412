## hw/urls.py
## description: the app-specofoc URLS for the hr application 

from django.urls import path # path funtion to associate string of url to function that actually does the url
from django.conf import settings
from . import views # 

#create a list of URLs for this app:

urlpatterns = [
    #path(r'', views.home, name="home"), # give name that matches the function name; This is our first URL; 
    path(r'', views.ShowRandomArticle.as_view(), name="random"),
    path(r'show_all', views.ShowAllView.as_view(), name="show_all"),
    path(r'article/<int:pk>', views.ArticleView.as_view(), name="article"),
    path('article/<int:pk>/create_comment', views.CreateCommentView.as_view(), name='create_comment'), ### NEW
    path(r'create_article', views.CreateArticleView.as_view(), name="create_article")
]