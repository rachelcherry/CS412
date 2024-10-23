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
        '''Return status_messages of this Profile.'''

        status_messages = StatusMessage.objects.filter(profile=self).order_by('timestamp')
        return status_messages
    def get_absolute_url(self):
        '''Return get_absolute_url of this Profile.'''
        return reverse('profile', kwargs={'pk': self.pk})
    def get_friends(self):
        '''Return friends of this Profile.'''
        return list(Friend.objects.filter(profile1=self)) | list(Friend.objects.filter(profile2=self))


class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.message} (created at {self.timestamp})"
    
    def get_images(self):
        status_images = Image.objects.filter(status_message=self)
        return status_images


class Image(models.Model):
    image_file = models.ImageField(blank=True) 
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)


class Friend(models.Model):
    anniversary = models.DateTimeField(auto_now=True)
    profile1 = models.ForeignKey(Profile, related_name="profile1", on_delete=models.CASCADE)
    profile2 = models.ForeignKey(Profile, related_name="profile2", on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.profile1} & {self.profile2}"

