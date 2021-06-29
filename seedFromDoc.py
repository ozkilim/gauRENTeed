# 1.Import csv or xlsx data from data collection
from gauRENTeed import settings
import pandas as pd
from beta.models import Property, Review
import os

import sys
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'gauRENTeed.settings'
django.setup()
path = "/Users/ozkilim/Documents/gauRENTeed/sourceData/Cleaned Redland Renting Experience  (Responses,cleaned) - Form responses 1.csv"

df = pd.read_csv(path)


def seeder():
    for index, row in df.iterrows():
        fullAddress = row[1]
        postcode = row[2]
        # Seed new objcts in db
        # Check for duplicates
        if Property.objects.filter(fullAddress=fullAddress) != fullAddress:
            newProperty = Property(fullAddress=fullAddress, postcode=postcode)
            newProperty.save()
    # seed a new house if it does not exist....
    # Process each row
# The above two lines could be written simply as:
# from project.wsgi import *
## Need to mke custom ocmmnd