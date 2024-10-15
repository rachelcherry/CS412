from django.db import models
#define data models (objects) for use in the blog application
# Create your models here.
class Article(models.Model):
    '''Encapsulate the idea of a Article by some author.'''
    # data attributes of a Article:
    title = models.TextField(blank=False)
    author = models.TextField(blank=False, default='Unknown Author')
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True) ## new
    
    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.title} by {self.author}'
    def get_comments(self):
        '''Return all of the comments about this article.'''
        comments = Comment.objects.filter(article=self)
        return comments
class Comment(models.Model):
    '''Encapsulate a comment on an article'''
   #create a 1 to many relationship between Articles and Comments 
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    def __str__(self):
        '''return string representation of this Article.'''
        return f"{self.text}"