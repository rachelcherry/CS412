from django.db import models
#define data models (objects) for use in the blog application
# Create your models here.
class Profile(models.Model):
    '''Encapsulate the data for a facebook profle.'''
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    image_url = models.URLField(blank=True)

    # def __str__(self):
    #     '''return string representation of this Article.'''
    #     return f"{self.title} by {self.author}"
