from django.db import models
from django.urls import reverse
# Define data models (objects) for use in the blog application
class Profile(models.Model):
    '''Encapsulate the data for a Facebook profile.'''
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    image_url = models.URLField(blank=True)

    def __str__(self):
        '''Return string representation of this Profile.'''
        return f"{self.first_name} {self.last_name}"
    def get_status_messages(self):
        status_messages = StatusMessage.objects.filter(profile=self).order_by('timestamp')
        return status_messages
    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})


class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.message} (created at {self.timestamp})"
