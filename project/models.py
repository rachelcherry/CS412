from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Avg
from django.urls import reverse
import random
import datetime
import time
from bs4 import BeautifulSoup
import requests
from django.db.models.functions import Round
# Create your models here.

# Rachel Cherry
# rcherry@bu.edu
# project/models.py
# Date created: November 12, 2024
# this file handles all of the models for the application
class Person(models.Model):
    '''model to define a person/profile in the application'''
    # first name of the person; required field
    first_name = models.TextField(blank=False) 
     # last name of the person; required field
    last_name = models.TextField(blank=False) 
    # address of the person; required field
    address = models.TextField(blank=False)  
    # date of birth of person
    dob = models.DateField() 
    # email of the person which is a required field
    email = models.TextField(blank=False) 
    # image of a person which is an optional field
    image_url = models.URLField(blank=True) 
     # created a one to one relationship with the built in django model 
    user = models.OneToOneField(User, on_delete=models.CASCADE)

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
        # finds whether the current person is profile1 or profile2 from the Friend model
        which_friend = Friend.objects.filter(profile1=self) | Friend.objects.filter(profile2=self)  
        # create a list of all the friends of this person
        allprofiles = [] 
        # loop through the various friends
        for currentfriend in which_friend:
            # if the friend is the person (themselves), add the other friend (profile2) 
            if currentfriend.profile1 == self: 
                allprofiles.append(currentfriend.profile2)
            else:
                 # otherwise add profile1
                allprofiles.append(currentfriend.profile1)
         # return the list of all the person's friends
        return allprofiles
    def get_friend_suggestions(self):
        '''get friend suggestions to this Profile.'''
        #using list comprehension for each friend in the list of frieneds generated in the get_friends function
        friendships = [friend.pk for friend in self.get_friends()] 
        # add themselves to the list of friends as well since a person should not get a suggestion to add themselves as a friend
        friendships.append(self.pk) 
        # exclude friends that are already in friendships
        what_friends = Person.objects.exclude(pk__in=friendships) 
        # return the list of friends in a list
        return list(what_friends) 
    def get_news_feed(self):
        '''get recommendation feed for this Person'''
        # find the friends of the person
        prof_friends = self.get_friends() 
        # find the recommendations created by any of the person's friends
        friends_feed = Recommendation.objects.filter(person__in=prof_friends) 
        # return the list of the recommendations 
        return list(friends_feed) 
    def add_friend(self, other):
        '''add friends to this Person'''
        # get the list of friends for the person
        existing_friend = self.get_friends() 
        # if self and other are the same, disallow 
        if self == other: 
            print("not allowed to be friends with yourself")
        elif other in existing_friend: 
            # if they are already friends with the usre, do not suggest them as an addition
            print("not good")
        else:
            # add a friend model for the person and their new friend
            f = Friend(profile1=self, profile2=other) 
            # save it to the database
            f.save() 
            print("success")



class Entertainment(models.Model):
    '''model to define an entertainment'''
     # id of the entertainment that can be max 20 length 
    show_id = models.CharField(max_length=20) 
     # title of entertainment 
    title = models.TextField()
     # cast for the entertainment
    cast = models.TextField()
    # country where the entertainment was made
    country = models.TextField() 
     # date when the movie/show was added to Netflix
    date_added = models.TextField()
    # year the show / movie was released 
    release_year = models.IntegerField() 
    # rating of the movie/show such as PG-13, PG, etc.
    rating = models.CharField(max_length=6) 
     # director where only movies have director so it is not a required field
    director = models.TextField(blank=True, null=True)
    # type of the entertainment
    type = models.TextField() 
     # duration of the show/movie on Netflix
    duration = models.TextField()
    # where the entertainment is listed
    listed_in = models.TextField() 
    # description of the movie/show 
    description = models.TextField() 
     # trailer for the entertainment from YouTube
    trailer = models.URLField(blank=True, null=True)
    def get_recommendation(self):
        '''Return recommendations of of this entertainment'''
        # all the recommendations for this entertainment ordered by when they are created
        recs = Recommendation.objects.filter(entertainment=self).order_by('timestamp') 
        # return all the recommendations
        return recs
    def __str__(self):
        '''return to string for an entertainment '''
        return f"{self.title}"
    def get_rotten(self):
        '''function to return the title with underscores for use in rotten tomato url'''
        # perform series of replacements so that the url can properly be forms
        self.title = self.title.replace(':', '') # replace all colons
        self.title = self.title.replace('!', '') # replace all !
        self.title = self.title.replace('?', '') # replace all ?
        self.title = self.title.replace('-', '') # replace all dashes
        # replace spaces with underscores to be in the format of the rotten tomatoes url
        return self.title.replace(' ', '_') 
    def get_trailer(self):
        '''function to use web scraping to get the trailer from a google search'''
         # google searches cannot handle ampersands so replace them
        if '&' in self.title: 
            self.title = self.title.replace('&', 'and') 
        # search for the movie name and trailer 
        search_query = self.title + " trailer" 
         # replace spaces with plus sign
        query = search_query.replace(' ', '+')
        # this is the url where the scraping should take place
        google_url = f"https://www.google.com/search?q={query}" 
         # get the specific page needed
        page = requests.get(google_url)
        # use beautiful soup for web scraping
        soup = BeautifulSoup(page.content, "html.parser") 
        # find the link tags
        links = soup.findAll('a')
        #print(links)
        # loop through all of the a tags
        for link in links: 
            # find the actual links
            attr_list = link.get_attribute_list('href') 
            # see if any of them match the watch links 
            if "youtube.com/watch" in attr_list[0]: 
                # split on the ampersands to get the proper url
                video_url = attr_list[0].split('&')[0] 
                # split again on q= to get the part of the url necessary for embedding
                video_url = video_url.split('q=')[1] 
                # replace acii with special characters
                video_url = video_url.replace('%3F', '?') 
                # replace ascii with special characters 
                video_url = video_url.replace('%3D', '=') 
                return video_url # return the scraped url 

 



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
    # foreign key to the person model 
    person = models.ForeignKey(Person, on_delete=models.CASCADE) 
     # foreign key to the entertainment model
    entertainment = models.ForeignKey(Entertainment, on_delete=models.CASCADE)
     # thoughts about the movie/show
    thoughts = models.TextField(blank=True)
     # an integer rating of the movie/show
    rating = models.IntegerField()
    # would the user recommend this to others or now 
    recommend = models.BooleanField() 
     # timestsamp for the creation of the recommendation
    timestamp = models.DateTimeField(auto_now = True)
    def __str__(self):
        '''return to-string representation'''
        return f"{self.thoughts} by {self.person} and for {self.entertainment} at {self.timestamp}"
    def get_images(self):
        '''returns images for a given recommendation'''
        # find the images that match the recommendation
        rec_images = Image.objects.filter(recommendation=self) 
        # return the images 
        return rec_images 
class Friend(models.Model):
    '''model to define a friend'''
    # anniversary of the friendship
    anniversary = models.DateTimeField(auto_now=True) 
    # foreign key to person
    profile1 = models.ForeignKey(Person, related_name="profile1", on_delete=models.CASCADE) 
     # foreign key to person
    profile2 = models.ForeignKey(Person, related_name="profile2", on_delete=models.CASCADE)
    def __str__(self):
        '''return to-string representation of a friendship'''
        return f"{self.profile1} & {self.profile2}"
   
class Image(models.Model):
    '''model to define images'''
    # imagefield for uploading images associated with recommendations
    image_file = models.ImageField(blank=True) 
     # foreign key to recommendation
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
    # timestamp for the creation of the image 
    timestamp = models.DateTimeField(auto_now=True) 

def gen_rec():
    '''function to auto-create 3 recommendations for the first 100 movies/shows '''

    # this function is intended to make it easier to do the top 10 and top 5 list. Without this, I would have to manually input the recommendations

    # delete existing records to prevent duplicated 
    Recommendation.objects.all().delete() 
    # get the first 100 movies/tv shows
    entertainments = Entertainment.objects.all()[:100] 
    # obtain all the people so we can attach one to each of the recommendations
    persons = Person.objects.all() 
    # loop through all of the 100 entertainments
    for entertainment in entertainments: 
        # create 3 recommendations per entertainment 
        for i in range(3): 
             # choose a random profile to assign the person attribute to
            person = random.choice(persons)
            # create a new Recommendation model with the person, entertainment, the same message, a random rating, and the current timestamp
            recommendation = Recommendation(
                person=person,
                entertainment=entertainment,
                thoughts="This was great!",
                rating=random.randint(1, 5),
                recommend=True,
                timestamp=datetime.datetime.now()
               
            )
             # save all of these recommendations to the database 
            recommendation.save()
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
        # reverse is True because we want the list in order of the highest rating to the lowest rating
        sorted_list = sorted(vals, key=lambda top_5: top_5[1], reverse=True) 
         # only take the top 5 from each month
        top_5[month] = sorted_list[:5] 
    # return the months and their top 5 entertainments
    return top_5 




def load_trailers():
    # loop through 10 entertainments at a time (right now until 1000)
    for entertainment in Entertainment.objects.all()[990:1000]:
        trailer_url = entertainment.get_trailer()
        # print(trailer_url)
        # switch the url to the structure needed for embedding
        embed_url = trailer_url.replace("watch?v=", "embed/") 
        # print(embed_url)
        # set the trailer attribute to be the embedded url 
        entertainment.trailer = embed_url
        # save the entertainment with the new url 
        entertainment.save()