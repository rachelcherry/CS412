from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Avg
from django.urls import reverse
import random
import datetime
from bs4 import BeautifulSoup
import requests
from django.db.models.functions import Round
# Create your models here.

# Rachel Cherry
# rcherry@bu.edu
# project/models.py
class Person(models.Model):
    '''model to define a person/profile in the application'''
    first_name = models.TextField(blank=False) # first name of the person; required field
    last_name = models.TextField(blank=False)  # last name of the person; required field
    address = models.TextField(blank=False)  # address of the person; required field
    dob = models.DateField() # date of birth of person
    email = models.TextField(blank=False) # email of the person which is a required field
    image_url = models.URLField(blank=True) # image of a person which is an optional field
    user = models.OneToOneField(User, on_delete=models.CASCADE) # created a one to one relationship with the built in django model 
    def get_recommendation(self):
        '''Return recommendations of this Person.'''
        # filter recommendations to find the recommendations that match the person
        recs = Recommendation.objects.filter(person=self)
        return recs
    def __str__(self):
        '''Returns string representation of Person.'''

        return f"{self.first_name} {self.last_name}"
    def get_absolute_url(self):
        '''Return get_absolute_url of this person.'''
        # use reverse to return the url for the person with their primary key
        return reverse('person', kwargs={'pk': self.pk})
    def get_friends(self):
        '''Return friends of this Person.'''
        which_friend = Friend.objects.filter(profile1=self) | Friend.objects.filter(profile2=self)  # finds whether the current person is profile1 or profile2 from the Friend model
        allprofiles = [] # create a list of all the friends of this person
        for currentfriend in which_friend: # loop through the various friends
            if currentfriend.profile1 == self: # if the friend is the person (themselves), add the other friend (profile2)
                allprofiles.append(currentfriend.profile2)
            else:
                allprofiles.append(currentfriend.profile1) # otherwise add profile1
        return allprofiles # return the list of all the person's friends
    def get_friend_suggestions(self):
        '''get friend suggestions to this Profile.'''
        friendships = [friend.pk for friend in self.get_friends()] #using list comprehension for each friend in the list of frieneds generated in the get_friends function
        friendships.append(self.pk) # add themselves to the list of friends as well since a person should not get a suggestion to add themselves as a friend
        what_friends = Person.objects.exclude(pk__in=friendships) # exclude friends that are already in friendships
        return list(what_friends) # return the list of friends in a list
    def get_news_feed(self):
        '''get recommendation feed for this Person'''
        prof_friends = self.get_friends() # find the friends of the person
        friends_feed = Recommendation.objects.filter(person__in=prof_friends) # find the recommendations created by any of the person's friends
        return list(friends_feed) # return the list of the recommendations 
    def add_friend(self, other):
        '''add friends to this Person'''
        existing_friend = self.get_friends() # get the list of friends for the person
        if self == other: # if self and other are the same, disallow 
            print("not allowed to be friends with yourself")
        elif other in existing_friend: # if they are already friends with the usre, do not suggest them as an addition
            print("not good")
        else:
            f = Friend(profile1=self, profile2=other) # add a friend model for the person and their new friend
            f.save() # save it to the database
            print("success")



class Entertainment(models.Model):
    '''model to define an entertainment'''
    show_id = models.CharField(max_length=20)  # id of the entertainment that can be max 20 length 
    title = models.TextField() # title of entertainment 
    cast = models.TextField() # cast for the entertainment
    country = models.TextField() # country where the entertainment was made
    date_added = models.TextField() # date when the movie/show was added to Netflix
    release_year = models.IntegerField() # year the show / movie was released 
    rating = models.CharField(max_length=6) # rating of the movie/show such as PG-13, PG, etc.
    director = models.TextField(blank=True, null=True) # director where only movies have director so it is not a required field
    type = models.TextField() # type of the entertainment
    duration = models.TextField() # duration of the show/movie on Netflix
    listed_in = models.TextField() # where the entertainment is listed
    description = models.TextField() # description of the movie/show 
    trailer = models.URLField(blank=True, null=True) # trailer for the entertainment from YouTube
    def get_recommendation(self):
        '''Return recommendations of of this entertainment'''
        recs = Recommendation.objects.filter(entertainment=self) # all the recommendations for this entertainment
        return recs # return all the recommendations
    def __str__(self):
        '''return to string for an entertainment '''
        return f"{self.title}"
    def get_rotten(self):
        '''function to return the title with underscores for use in url'''
        self.title = self.title.replace(':', '')
        self.title = self.title.replace('!', '')
        self.title = self.title.replace('?', '')
        self.title = self.title.replace('-', '')
        return self.title.replace(' ', '_')
    def get_trailer(self):
        if '&' in self.title:  
            self.title = self.title.replace('&', 'and') 
        search_query = self.title + " trailer"
        query = search_query.replace(' ', '+')
        google_url = f"https://www.google.com/search?q={query}"
        print(google_url)
        page = requests.get(google_url)
        soup = BeautifulSoup(page.content, "html.parser")
        links = soup.findAll('a')
        #print(links)
        for link in links:
            attr_list = link.get_attribute_list('href')
            if "youtube.com/watch" in attr_list[0]:
                video_url = attr_list[0].split('&')[0]
                video_url = video_url.split('q=')[1]
                video_url = video_url.replace('%3F', '?')
                video_url = video_url.replace('%3D', '=')
                return video_url

 



def load_data():
    '''Function to load data records from CSV file into Django model instances.'''
    # delete existing records to prevent duplicates:
    Entertainment.objects.all().delete()
    # establish the source where the data is going to be loaded from 
    filename = '/Users/rachelcherry/Desktop/412/netflix_titles.csv'
    # open the file for reading
    with open(filename) as f:
        # get rid of the headers 
        f.readline()
        # go through each line in the data table
        for line in f:
            # split on the commas 
            fields = line.strip().split(',')
            try:
                # create an Entertainment model with the fields from the data table 
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
                    description=fields[11],
                    
                )
                # save the results to the database 
                result.save()
                print(f'Created result: {result}')
             # if the creation of the model fails, print the error   
            except Exception as e:
                print(f"Skipped: {fields} - Error: {e}")
    
    
    print(f'Done. Created {Entertainment.objects.count()} Shows.')


class Recommendation(models.Model):
    '''model to define a recommendation'''
    person = models.ForeignKey(Person, on_delete=models.CASCADE) # foreign key to the person model 
    entertainment = models.ForeignKey(Entertainment, on_delete=models.CASCADE) # foreign key to the entertainment model
    thoughts = models.TextField(blank=True) # thoughts about the movie/show
    rating = models.IntegerField() # an integer rating of the movie/show
    recommend = models.BooleanField() # would the user recommend this to others or now 
    timestamp = models.DateTimeField(auto_now = True) # timestsamp for the creation of the recommendation
    def __str__(self):
        '''return to-string representation'''
        return f"{self.thoughts} by {self.person} and for {self.entertainment} at {self.timestamp}"
    def get_images(self):
        '''returns images for a given recommendation'''
        rec_images = Image.objects.filter(recommendation=self) # find the images that match the recommendation
        return rec_images # return the images 
class Friend(models.Model):
    '''model to define a friend'''
    anniversary = models.DateTimeField(auto_now=True) # anniversary of the friendship
    profile1 = models.ForeignKey(Person, related_name="profile1", on_delete=models.CASCADE) # foreign key to person
    profile2 = models.ForeignKey(Person, related_name="profile2", on_delete=models.CASCADE) # foreign key to person
    def __str__(self):
        '''return to-string representation of a friendship'''
        return f"{self.profile1} & {self.profile2}"
   
class Image(models.Model):
    '''model to define images'''
    image_file = models.ImageField(blank=True) # imagefield for uploading images associated with recommendations
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE) # foreign key to recommendation
    timestamp = models.DateTimeField(auto_now=True) # timestamp for the creation of the image 

def gen_rec():
    '''function to auto-create 3 recommendations for the first 100 movies/shows '''

    # this function is intended to make it easier to do the top 10 and top 5 list. Without this, I would have to manually input the recommendations

    Recommendation.objects.all().delete() # delete existing records to prevent duplicated 

    entertainments = Entertainment.objects.all()[:100] # get the first 100 movies/tv shows
    persons = Person.objects.all() # obtain all the people so we can attach one to each of the recommendations

    for entertainment in entertainments: # loop through all of the 100 entertainments
        for i in range(3): # create 3 recommendations per entertainment 
            person = random.choice(persons) # choose a random profile to assign the person attribute to
            # create a new Recommendation model with the person, entertainment, the same message, a random rating, and the current timestamp
            recommendation = Recommendation(
                person=person,
                entertainment=entertainment,
                thoughts="This was great!",
                rating=random.randint(1, 5),
                recommend=True,
                timestamp=datetime.datetime.now()
               
            )
            recommendation.save() # save all of these recommendations to the database 
    print("Done")

def top_10():
    '''this function will find the top 10 most highly rated entertainments in the application'''
    top_100 = Entertainment.objects.all()[:100] # get the first 100 entertainments
    top_10 = [] # create an empty list to hold the values 
    # loop through the first 100 entertainments 
    for entertainment in top_100:
        # get the recommendations for the current entertainment
        recommendations = Recommendation.objects.filter(entertainment=entertainment)
        # take the average of the rating for each of the entertainment objects
        avg_rating = round(recommendations.aggregate(Avg('rating'))['rating__avg'], 2)
        # add these ratings and their associated entertainment to a list called top_10
        top_10.append((entertainment, avg_rating))
    # now, we can sort by the rating (which is the second postion of the array) so that they are in order
    top_10_sorted = sorted(top_10, key=lambda top10: top10[1], reverse=True) # use reverse so it is highest rating to lowest rating 
    # finally, we want to only return the top 10 movies, so we slice our array to only include the first 10 positions in the sorted array 
    return top_10_sorted[:10]

def top_5():
    '''this function will find the top 5 most highly rated entertainments in the application per month they were created'''

    top_100 = Entertainment.objects.all()[:100] # take the first 100 entertainment object
    top_5 = {} # create a dictionary to hold the top 5
    groups = {} # create another dictionary to hold the months and recommendations
    # loop through the first 100 entertainments 
    for entertainment in top_100:
        # get all the recommendations for this entertainment
        recommendations = Recommendation.objects.filter(entertainment=entertainment)
        # find the average rating for the recommendations
        avg_rating = round(recommendations.aggregate(Avg('rating'))['rating__avg'], 2)
        print(avg_rating)
        # loop through the recommendations
        for rec in recommendations:
            # find the month associated with the timestamp of the recommendation
            month = rec.timestamp.month
            # check if the month is already created in the dictionary
            # if the month is not created, create a specific list for the month
            if month not in groups:
                groups[month] = []
            # create a boolean to indicate whether the entertainment is already in the list
            bool = False
            # loop through each value in the current month array
            for i in groups[month]:
                # if the title is equal to the entertainment currently being looked at, break out of the loop because we do not want to add it to the list again
                if i[0] == entertainment:
                    bool = True
                    break
            # if the entertainment title has not been added yet, then we add it along with it's average rating
            if not bool: 
                groups[month].append((entertainment, avg_rating))
    # loop through and sort the values within each month
    for month, vals in groups.items():
        sorted_list = sorted(vals, key=lambda top_5: top_5[1], reverse=True) # reverse is True because we want the list in order of the highest rating to the lowest rating
        top_5[month] = sorted_list[:5]  # only take the top 5 from each month
    return top_5 # return the months and their top 5 entertainments


import time

def load_trailers():
    count = 0  # Track the number of requests
    for entertainment in Entertainment.objects.all()[990:1000]:
        trailer_url = entertainment.get_trailer()
        # print(trailer_url)
        embed_url = trailer_url.replace("watch?v=", "embed/") 
        # print(embed_url)
        entertainment.trailer = embed_url
        entertainment.save()
        print(trailer_url)