from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Define data models (objects) for use in the blog application
class Profile(models.Model):
    '''Encapsulate the data for a Facebook profile.'''
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    image_url = models.URLField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


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
        which_friend = Friend.objects.filter(profile1=self) | Friend.objects.filter(profile2=self)
        allprofiles = []
        for currentfriend in which_friend:
            if currentfriend.profile1 == self:
                allprofiles.append(currentfriend.profile2)
            else:
                allprofiles.append(currentfriend.profile1)
        return allprofiles
    def add_friend(self, other):
        '''add friends to this Profile.'''
        existing_friend = self.get_friends()
        print(self, other)
        print(existing_friend)
        if self == other:
            print("not allowed to be friends with yourself")
        elif other in existing_friend:
            print("not good")
        else:
            f = Friend(profile1=self, profile2=other)
            f.save()
            print("success")
    def get_friend_suggestions(self):
        '''get friend suggestions to this Profile.'''
        friendships = [friend.pk for friend in self.get_friends()]
        friendships.append(self.pk)
        what_friends = Profile.objects.exclude(pk__in=friendships)
        print(list(what_friends))
        return list(what_friends)
    def get_news_feed(self):
        '''get news feed for this Profile'''
        prof_friends = self.get_friends()
        prof_friends.append(self)
        friends_feed = StatusMessage.objects.filter(profile__in=prof_friends)
        return list(friends_feed)





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

    

