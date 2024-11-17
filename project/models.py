from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
class Person(models.Model):
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    address = models.TextField(blank=False)
    dob = models.DateField()
    email = models.TextField(blank=False)
    image_url = models.URLField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def get_recommendation(self):
        '''Return recommendations of this Person.'''
        recs = Recommendation.objects.filter(person=self)
        return recs
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    def get_friends(self):
        '''Return friends of this Person.'''
        which_friend = Friend.objects.filter(profile1=self) | Friend.objects.filter(profile2=self)
        allprofiles = []
        for currentfriend in which_friend:
            if currentfriend.profile1 == self:
                allprofiles.append(currentfriend.profile2)
            else:
                allprofiles.append(currentfriend.profile1)
        return allprofiles


class Entertainment(models.Model):
    show_id = models.CharField(max_length=20)  
    title = models.TextField()
    cast = models.TextField()
    country = models.TextField()
    date_added = models.TextField()
    release_year = models.IntegerField()
    rating = models.CharField(max_length=6)
    director = models.TextField(blank=True, null=True)
    type = models.TextField()
    duration = models.TextField()
    listed_in = models.TextField()
    description = models.TextField()
    def get_recommendation(self):
        '''Return recommendations of this Profile.'''
        recs = Recommendation.objects.filter(entertainment=self)
        return recs
    def __str__(self):
        return f"{self.title}"

def load_data():
    '''Function to load data records from CSV file into Django model instances.'''
    # delete existing records to prevent duplicates:
    Entertainment.objects.all().delete()
    
    filename = '/Users/rachelcherry/Desktop/412/netflix_titles.csv'
    with open(filename) as f:
        f.readline()
        for line in f:
            fields = line.strip().split(',')
            try:
      
                result = Entertainment(
                    show_id=fields[0],
                    type = fields[1],
                    title=fields[2],
                    director=fields[3] if fields[3] else None,
                    cast=fields[4],
                    country=fields[5],
                    date_added=fields[6],
                    release_year=fields[7],
                    rating=fields[8],
                    duration=fields[9],
                    listed_in=fields[10],
                    description=fields[11]
                    
                )
                result.save()
                print(f'Created result: {result}')
                
            except Exception as e:
                print(f"Skipped: {fields} - Error: {e}")
    
    
    print(f'Done. Created {Entertainment.objects.count()} Voters.')



class Recommendation(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    entertainment = models.ForeignKey(Entertainment, on_delete=models.CASCADE)
    thoughts = models.TextField(blank=True)
    rating = models.IntegerField()
    recommend = models.BooleanField()
    def __str__(self):
        return f"{self.thoughts} by {self.person} and for {self.entertainment}"
class Friend(models.Model):
    anniversary = models.DateTimeField(auto_now=True)
    profile1 = models.ForeignKey(Person, related_name="profile1", on_delete=models.CASCADE)
    profile2 = models.ForeignKey(Person, related_name="profile2", on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.profile1} & {self.profile2}"
    
