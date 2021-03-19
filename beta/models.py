from django.db import models
from django.template.defaultfilters import slugify
# from django.contrib.auth.models import User
from django.urls import reverse
from django.forms import ModelForm
from django import forms


# The landlord adds the property here...WOuld we wnt to seed ourselves..?to start..

# These are the objective facts about the property nearest station is added by us?... with logic..with google map api
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    send_daily_emails = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class Property(models.Model):
    address = models.CharField(max_length=255)
    rent = models.IntegerField()
    size = models.IntegerField()
    buildDate = models.DateTimeField(auto_now_add=True)
    # add usefull but objective info
    livingNumber = models.IntegerField()
    nearestStation = models.TextField()


class Review(models.Model):
    consent = models.BooleanField(default=True,
                                  help_text='Are you happy for us to anonymously upload your review to our property review site? Your review will be anonymised')

    livingConfirmation = models.BooleanField(default=True,
                                             help_text='Do you confirm that you live or lived at the property in question?')

    firstName = models.CharField(max_length=255)

    contactPermisssion = models.BooleanField(default=True,
                                             help_text='Do you want us to contact you when we upload your review?')

    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, default=None)

    reviewDate = models.DateField(
        auto_now_add=True)

    moveIn = models.DateField(auto_now_add=False
                              )

    moveOut = models.DateField(auto_now_add=False,
                               )

    USER_OCCUPATION_CHOICES = [
        ("Student", "Student"), ("Non student", "Non student")]

    occupation = models.CharField(
        choices=USER_OCCUPATION_CHOICES, default="Student", max_length=255
    )

    BEDROOM_NUMBER_CHOICES = [
        (1, 1), (2, 2,), (3, 2), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)]

    bedroomNumber = models.IntegerField(
        choices=BEDROOM_NUMBER_CHOICES, default=3, help_text='How many bedrooms was the house? ')

    RATING_CHOICES = [
        (1, 1), (2, 2,), (3, 2), (4, 4), (5, 5)
    ]

    overallRating = models.IntegerField(
        choices=RATING_CHOICES,
        default=3, help_text='How would you rate the property out of 5? [conditon, responsiveness of landlord/property management company/value for money/neighbourhood]'
    )

    overallMaintainance = models.IntegerField(
        choices=RATING_CHOICES,
        default=3, help_text='What was the condition of the property and how well was it maintained? '
    )

    buildingQuality = models.IntegerField(
        choices=RATING_CHOICES,
        default=3, help_text='What was the quality of the building [considering pests, rodents, cleanliness and any damp or mould]?'
    )
    furnishings = models.IntegerField(
        choices=RATING_CHOICES,
        default=3, help_text='What was the quality of the furnishings? '
    )

    water = models.IntegerField(
        choices=RATING_CHOICES,
        default=3, help_text='How would you rate the water, heating and insulation of the property?'
    )

    whiteGoods = models.IntegerField(
        choices=RATING_CHOICES,
        default=3, help_text='How would you rate the quality of the white goods (dishwasher, washing machine, electrical appliances)'
    )

    maintainanceComment = models.CharField(
        null=True, blank=True, help_text='Any other comment?', max_length=255)

    overallLandlord = models.IntegerField(
        choices=RATING_CHOICES,
        default=3, help_text='How would you rate the landlord/property management company?'
    )
    responsiveness = models.IntegerField(
        choices=RATING_CHOICES,
        default=3, help_text='How responsive was the landlord/property management company to an issues that were raised? '
    )
    repairQuality = models.IntegerField(
        choices=RATING_CHOICES,
        default=3, help_text='How would you rate the quality of any repairs to any issues raised?'
    )
    movingInExperiance = models.IntegerField(
        choices=RATING_CHOICES,
        default=3, help_text='How would you rate the moving in process and experience? [Moving in dates, state of property etc] '
    )
    movingOutExperiance = models.IntegerField(
        choices=RATING_CHOICES,
        default=3, help_text='How would you rate the moving out process and experience? [Deposit, cleanling fees, fairness] '
    )

    landlordComment = models.CharField(
        null=True, blank=True, help_text='Any other comment?', max_length=255)

    rent = models.PositiveIntegerField(
        default=500, help_text='What was your monthly rent?')

    valueForMoney = models.BooleanField(default=True,
                                        help_text='Was the property worth the money?')

    areaSafety = models.IntegerField(
        choices=RATING_CHOICES,
        default=3, help_text='How safe did you feel in the area?'
    )

    areaEnjoyment = models.IntegerField(
        choices=RATING_CHOICES,
        default=3, help_text='How much did you enjoy living in the area? '
    )
    areaEnjoymentReason = models.CharField(
        null=True, blank=True, help_text='why? [amenities, closeness to transport, noise]', max_length=255)

    recomendation = models.BooleanField(default=True,
                                        help_text='Would you reccomend this property to others? ')


class ReviewProduct(models.Model):
    name        = models.CharField(max_length=234)
    year        = models.CharField(max_length=4)
    charge_id   = models.CharField(max_length=234)