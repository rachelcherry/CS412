from django.db import models
#define data models (objects) for use in the blog application
# Create your models here.
class Article(models.Model):
    '''Encapsulate the data for a blog Article by some author.'''
    title = models.TextField(blank=False) # cannot create a model without a title
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True) # sets the current published time to now 
    image_url = models.URLField(blank=True) ## new field

    def __str__(self):
        '''return string representation of this Article.'''
        return f"{self.title} by {self.author}"
