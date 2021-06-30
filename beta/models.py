from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify
# from django.contrib.auth.models import User
from django.urls import reverse
from django.forms import ModelForm
from django import forms

import os
import time
import hashlib
from os import path
from binascii import hexlify
from django.db import models
from django.contrib import admin
from django.core.files.storage import FileSystemStorage
import hashlib
import random
import uuid

from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    send_daily_emails = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class Property(models.Model):
    fullAddress = models.CharField(
        unique=True, max_length=255, default="", blank=True)

    postcode = models.CharField(
        unique=False, max_length=255, default="", blank=True)

    hashId = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.fullAddress

    def save(self, *args, **kwargs):
        self.fullAddress = self.fullAddress
        super(Property, self).save(*args, **kwargs)


class Review(models.Model):

    verified = models.BooleanField(default=False)

    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, default=None)

    reviewDate = models.DateField(
        auto_now_add=True)

    RATING_CHOICES = [
        (1, 1), (2, 2,), (3, 3), (4, 4), (5, 5)
    ]
    timeStamp = models.CharField(
        null=True, blank=True, help_text='Time data was collected', max_length=255)

    livingConfirmation = models.BooleanField(default=True, blank=True,
                                             help_text='Do you confirm that you live or lived at the property in question?')

    moveIn = models.DateField(auto_now_add=False, null=True,
                              )

    moveOut = models.DateField(auto_now_add=False, null=True,
                               )

    BEDROOM_NUMBER_CHOICES = [
        (1, 1), (2, 2,), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)]

    bedroomNumber = models.IntegerField(null=True, blank=True,
                                        choices=BEDROOM_NUMBER_CHOICES, default=3, help_text='How many bedrooms was the house? ')

    USER_OCCUPATION_CHOICES = [
        ("Student", "Student"), ("Employed", "Employed"), ("Self-Employed", "Self-Employed")]

    employmentStatus = models.CharField(null=True,
                                        choices=USER_OCCUPATION_CHOICES, default="Student", max_length=255
                                        )

    reviewerName = models.CharField(max_length=255, null=True)

    buildingQuality = models.IntegerField(null=True, blank=True,
                                          choices=RATING_CHOICES,
                                          default=3, help_text='How would you rate the quality of the building (considering mould, pests, cleanliness, damp, etc.)?')

    buildigComment = models.CharField(
        null=True, blank=True, help_text='Can you explain why you have given it the rating that you have?', max_length=255)

    moveInHygene = models.IntegerField(null=True, blank=True,
                                       choices=RATING_CHOICES,
                                       default=3, help_text='When you moved in, how clean was the property?')

    moveInHygeneComment = models.CharField(
        null=True, blank=True, help_text='Can you explain why you have given it the rating that you have?', max_length=255)

    utilities = models.IntegerField(null=True, blank=True,
                                    choices=RATING_CHOICES,
                                    default=3, help_text='How would you rate the utilities? (water pressure, heating, insulation etc)')

    utilitiesComment = models.CharField(
        null=True, blank=True, help_text='Can you explain why you have given it the rating that you have?', max_length=255)

    bedroomQuality = models.IntegerField(null=True, blank=True,
                                         choices=RATING_CHOICES,
                                         default=3, help_text='What is the quality of the bedrooms at the property? (Size, comfort, privacy etc)')

    bedroomQualityComment = models.CharField(
        null=True, blank=True, help_text='Can you explain why you have given it the rating that you have?', max_length=255)

    furnishings = models.IntegerField(null=True, blank=True,
                                      choices=RATING_CHOICES,
                                      default=3, help_text='If the property was furnished, what is the quality of the furnishings like? (Beds, wardrobes, tables, sofas, etc.)')

    furnishingsComment = models.CharField(
        null=True, blank=True, help_text='Can you explain why you have given it the rating that you have?', max_length=255)

    manageResponsivenes = models.IntegerField(null=True, blank=True,
                                              choices=RATING_CHOICES,
                                              default=3, help_text='When you have a problem how responsive is the property manager? ')

    manageResponsivenesComment = models.CharField(
        null=True, blank=True, help_text='Can you explain why you have given them the rating that you have?', max_length=255)

    repairQuality = models.IntegerField(null=True, blank=True,
                                        choices=RATING_CHOICES,
                                        default=3, help_text='When the property manager arranges a repair, the repair is usually...')

    repairQualityComment = models.CharField(
        null=True, blank=True, help_text='Can you explain why you have given it the rating that you have?', max_length=255)

    hiddenExpenses = models.CharField(
        null=True, blank=True, help_text='Were there any hidden expenses at the end of the tenancy? (Cleaning costs, significant deposit reductions, unexpected charges, etc) ', max_length=255)

    wantedToKnowBefore = models.CharField(
        null=True, blank=True, help_text='Is there anything else you would have liked to have known about the property manager before you moved in?', max_length=255)

    rentMonthly = models.PositiveIntegerField(null=True,
                                              default=500, help_text='What is the total monthly rent for the property?')

    rentGoodDeal = models.BooleanField(default=True,
                                       help_text='Do you feel the total monthly rent is a good deal?')

    neighbourhoodDescription = models.CharField(
        null=True, blank=True, help_text='How would you describe the neighbourhood to someone thinking of living there?', max_length=255)

    neighbourhoodSafety = models.IntegerField(null=True, blank=True,
                                              choices=RATING_CHOICES,
                                              default=3, help_text='How safe do you feel in the neighbourhood?')

    neighbourhoodSafetyComment = models.CharField(
        null=True, blank=True, help_text='Can you explain why you have given it the rating that you have?', max_length=255)

    neighbourhoodEnjoyment = models.IntegerField(null=True, blank=True,
                                                 choices=RATING_CHOICES,
                                                 default=3, help_text='How much do you enjoy living in this area?')

    goodPlaceForFriends = models.IntegerField(null=True, blank=True,
                                              choices=RATING_CHOICES,
                                              default=3, help_text='My house was a good place to have friends over')

    goodPlaceForDinnerParties = models.IntegerField(null=True, blank=True,
                                                    choices=RATING_CHOICES,
                                                    default=3, help_text='My house was a good place to have dinner parties')

    enjoyedCooking = models.IntegerField(null=True, blank=True,
                                         choices=RATING_CHOICES,
                                         default=3, help_text='I enjoyed cooking in the kitchen')

    feltLikeAHome = models.IntegerField(null=True, blank=True,
                                        choices=RATING_CHOICES,
                                        default=3, help_text='It felt like a home')

    cosyInWinter = models.IntegerField(null=True, blank=True,
                                       choices=RATING_CHOICES,
                                       default=3, help_text='It was cosy in the winter')

    windowView = models.IntegerField(null=True, blank=True,
                                     choices=RATING_CHOICES,
                                     default=3, help_text='I enjoyed the view out of the windows')

    neighboursRelationship = models.IntegerField(null=True, blank=True,
                                                 choices=RATING_CHOICES,
                                                 default=3, help_text='I had a good relationship with my neighbours')

    study = models.IntegerField(null=True, blank=True,
                                choices=RATING_CHOICES,
                                default=3, help_text='It was good for studying and focus')

    easyToSleepAtNight = models.IntegerField(null=True, blank=True,
                                             choices=RATING_CHOICES,
                                             default=3, help_text='It was easy to sleep at night')

    feltSafe = models.IntegerField(null=True, blank=True,
                                   choices=RATING_CHOICES,
                                   default=3, help_text='I felt safe in my house')

    landlordRelationship = models.IntegerField(null=True, blank=True,
                                               choices=RATING_CHOICES,
                                               default=3, help_text='I had a good relationship with my landlord / estate agent')

    hotShower = models.IntegerField(null=True, blank=True,
                                    choices=RATING_CHOICES,
                                    default=3, help_text='I was able to have a hot shower whenever I wanted')

    likedMost = models.CharField(
        null=True, blank=True, help_text='What do/did you like most about the property?', max_length=255)

    likedLeast = models.CharField(
        null=True, blank=True, help_text='What do/did you like least about the property?', max_length=255)

    overallRating = models.IntegerField(null=True, blank=True,
                                        choices=RATING_CHOICES,
                                        default=3, help_text='Overall, how would you rate this property?')

    dataConsent = models.BooleanField(default=True, null=True,
                                      help_text='Are you happy for the data collected during this interview to appear anonymously as a property review on our website?')

    contactWhenDataPublic = models.BooleanField(default=True, null=True,
                                                help_text='Would you like to be contacted when this review is made public?')

    futuePaidWork = models.BooleanField(default=True, null=True,
                                        help_text='Would you like to hear about future opportunities to work as a paid ambassador for GuaRENTeed?')

    email = models.CharField(
        null=True, blank=True, help_text='email', max_length=255)

    ambassadorPotential = models.BooleanField(default=True, null=True,
                                              help_text='Would you like to be sent paid opportunities to be a GuaRENTeed ambassador?')

    whoSentSurvey = models.CharField(
        null=True, blank=True, help_text='Who sent you this survey? (Leave blank if you scanned the QR code on our leaflet)', max_length=255)

    maintenanceMoveIn = models.IntegerField(null=True, blank=True,
                                            choices=RATING_CHOICES,
                                            default=3, help_text='MAINTENANCE/CONDITION: How would you rate the condition of the property when you moved in?')

    whiteGoods = models.IntegerField(null=True, blank=True,
                                     choices=RATING_CHOICES,
                                     default=3, help_text='MAINTENANCE/CONDITION: What was the quality of the white goods (dishwasher, washing machine etc)')

    qualityComments = models.CharField(
        null=True, blank=True, help_text='Any other comment about the quality of property?', max_length=255)

    landlordRating = models.IntegerField(null=True, blank=True,
                                         choices=RATING_CHOICES,
                                         default=3, help_text='LANDLORD: Any other comments')

    landlordComments = models.CharField(
        null=True, blank=True, help_text='LANDLORD: Any other comments', max_length=255)

    areaBenefits = models.CharField(
        null=True, blank=True, help_text='What were the benefits of the area?', max_length=255)

    areaPerks = models.CharField(
        null=True, blank=True, help_text='Perks of area', max_length=255)

    wouldRecommendProperty = models.BooleanField(default=True, null=True,
                                                 help_text='Would you reccomend this property to others? ')

    def __str__(self):
        return self.reviewerName + self.property.fullAddress + " review"


class ReviewProduct(models.Model):
    name = models.CharField(max_length=234)
    year = models.CharField(max_length=4)
    charge_id = models.CharField(max_length=234)

# Model for user to store their fav places and compare one against another. NOT IN MVP
# class MyList(models.Model):
#     name = models.CharField(max_length=234)
#     year = models.CharField(max_length=4)
#     charge_id = models.CharField(max_length=234)
