from django.db import models
import os
class Voter(models.Model):
    # identification
    voter_id = models.CharField(max_length=20)  
    last_name = models.TextField()
    first_name = models.TextField()
    street_number = models.TextField()
    street_name = models.TextField()
    apt_number = models.TextField(null=True, blank=True)
    zip_code = models.TextField()
    dob = models.DateField()
    registration_date = models.DateField()
    party_affiliation = models.TextField()
    precinct_number = models.CharField(max_length=2)
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name}'

def load_data():
    '''Function to load data records from CSV file into Django model instances.'''
    # delete existing records to prevent duplicates:
    Voter.objects.all().delete()
    
    filename = '/Users/rachelcherry/Desktop/412/newton_voters.csv'
    with open(filename) as f:
        f.readline()
        for line in f:
            fields = line.strip().split(',')
            try:
                
                result = Voter(
                    voter_id=fields[0],
                    last_name=fields[1],
                    first_name=fields[2],
                    street_number=fields[3],
                    street_name=fields[4],
                    apt_number=fields[5] if fields[5] else None,
                    zip_code=fields[6],
                    dob=fields[7],
                    registration_date=fields[8],
                    party_affiliation=fields[9].strip(),
                    precinct_number=fields[10],
                    v20state=fields[11] == "TRUE",
                    v21town=fields[12] == "TRUE",
                    v21primary=fields[13] == "TRUE",
                    v22general=fields[14] == "TRUE",
                    v23town=fields[15] == "TRUE",
                    voter_score=fields[16],
                )
                result.save()
                print(f'Created result: {result}')
                
            except Exception as e:
                print(f"Skipped: {fields} - Error: {e}")
    
    print(f'Done. Created {Voter.objects.count()} Voters.')
