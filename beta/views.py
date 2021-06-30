import pandas as pd
import django
import sys
import os
from beta.models import Property, Review
import stripe
from jinja2 import *
from django.shortcuts import render
from django.contrib.auth.models import User
from beta.models import Property, Review, ReviewProduct
from beta.forms import ReviewForm, CustomUserCreationForm, CustomUser, PropertyCreationForm
# Create your views here.
from gauRENTeed import settings
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from gauRENTeed.middleware.login_exempt import login_exempt
from beta.tokens import account_activation_token
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import login
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers
from django.forms.models import model_to_dict
from django.http import JsonResponse
from formtools.wizard.views import SessionWizardView
from django.utils.dateparse import parse_datetime
import numpy as np
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.views import View


def landing(request):

    if request.method == 'POST':
        # get the searched result and redirect to correct page here
        fullAddress = request.POST.get('property')
        property = Property.objects.get(fullAddress=fullAddress)
        hashId = property.hashId
        return redirect('reasult', hashId=hashId)

    if 'term' in request.GET:
        qs = Property.objects.filter(
            fullAddress__icontains=request.GET.get('term'))
        fullAddress = []
        for property in qs:
            fullAddress.append(property.fullAddress)
        # return sorry if the reasult if not found
        if fullAddress == []:
            fullAddress = ["Sorry we don't have a review of this property yet"]
        return JsonResponse(fullAddress, safe=False)

    return render(request, 'landing.html')


def propertyList(request):
    # Get all properties in daatabase.
    properties = Property.objects.all()
    context = {'properties': properties}
    # Render the list of objects
    return render(request, 'propertyList.html', context=context)


def reasult(request, hashId):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    # if not logged in or not payed then popup directly for payment  easily.
    # context = {"stripe_key": settings.STRIPE_PUBLIC_KEY}
    # return render(request, "payment.html", context)
    # login popup then pay for login if not a user ..... all in modal..
    # Here decide if logged in...
    # if request.method == 'POST':
    #    return redirect('login')

    # Later will need to add hashing so users cannot get to the page for free
    property = Property.objects.get(hashId=hashId)
    # So user gets redirected to the review they wanted.
    urlsString = "beta/reasult/" + str(hashId)
    print(urlsString)
    # Get all properties
    # filter the get reviews for properties
    # Order the reviews by date from oldest to newest
    # Only display verified reviews....
    propertyReviews = Review.objects.filter(
        property=property, verified=True).order_by('reviewDate').values()

    if not propertyReviews:
        aggregateReview = ""
    else:
        allReviewList = [
            property["overallRating"] for property in propertyReviews]
        aggregateReview = sum(allReviewList)/len(allReviewList)

    context = {'property': property, 'reviews': propertyReviews,
               'aggregateReview': aggregateReview, "stripe_key": settings.STRIPE_PUBLIC_KEY, "urlsString": urlsString}
    return render(request, 'tempReasult.html', context)


def searchReasult(request):

    return render(request, 'searchReasult.html')


def review(request):
    # Get current reviews object

    propertyForm = PropertyCreationForm(request.POST)
    form = ReviewForm(request.POST)

    # CHANGE LOGIC FOR FULL ADRESS NOW!

    if request.method == 'POST':

        # Not best code as validation actuly fails when object already exists to is used as the check itself..
        if propertyForm.is_valid():
            # check if prprty object exists in our db
            address = propertyForm.cleaned_data['address']
            aptNumber = propertyForm.cleaned_data['aptNumber']
            addressCheck = Property.objects.filter(
                address=address, aptNumber=aptNumber).first()
            if not addressCheck:
                # search for this specific appt and address is in db
                addressCheck = propertyForm.save()

        print(propertyForm.errors)

        if form.is_valid():
            # set the review to be set onto the existing or created property
            # This NOT CHANGING VALUE!!!
            newReview = form.save(commit=False)
            newReview.property = addressCheck
            # THIS IS NOT AN  INSTANCE>>>
            # Not saving the review currently to back end....
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            # book_instance.due_back = form.cleaned_data['renewal_date']
            newReview.save()
            # add the property to the review
            # get the object

            # go back to home page
            return redirect('landing')

    context = {"form": form, "propertyForm": propertyForm}

    return render(request, 'tempReview.html', context=context)


def search(request):
    return render(request, 'search.html')


@ login_exempt
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_patient = True
            user.is_active = False
            user.save()
            '''hashing process here to give link'''
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            # fail here....
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')

            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            return render(request, 'confirm.html'
                          )  # should redirect to dead end page until user confirms email
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


@ login_exempt
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # flash message saying thanks
        return redirect('landing')
    else:
        return HttpResponse('Activation link is invalid!')
# the list will come in from the cam module...


@ login_exempt
def login(request):
    # Go to payment page or decide with the group
    # for now go to home..
    return render(request, 'login.html')


def logout(request):

    return render(request, 'landing.html')


def payment_form(request):

    context = {"stripe_key": settings.STRIPE_PUBLIC_KEY}
    return render(request, "payment.html", context)


def checkout(request):
    if request.method == 'POST':
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        # Pull out all data from first form...
        # Need some front end validation to ensure created object is correct.
        newUser = CustomUser(username=username, password=password,
                             email=email)
        newUser.is_patient = True
        newUser.is_active = True
        newUser.save()
        # Log this user in
        # user = authenticate(request, username=username, password=password)
        auth_login(request, newUser,
                   backend='django.contrib.auth.backends.ModelBackend')

        # Sed email back to this email automatically with their deails so they do not forget
        # Return to the page the user wanted....
        return redirect('landing')  # TO THE LOACTION THE USER WANTED


class FormWizardView(SessionWizardView):
    template_name = "wizardReview"
    form_list = [ReviewForm, PropertyCreationForm]

    def done(self, form_list):
        return render(self.request, 'wizardReview.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })


def aboutUs(request):
    return render(request, 'aboutUs.html')


def seeder(request):
    path = "/Users/ozkilim/Documents/gauRENTeed/sourceData/Cleaned Redland Renting Experience  (Responses,cleaned) - Form responses 1.csv"
    df = pd.read_csv(path)
    # Cut off top row...
    df = df[1:]
    df = df.replace({np.nan: None})
    for index, row in df.iterrows():
        fullAddress = row[1]
        postcode = row[2]
        # Seed new objcts in db
        # Check for duplicates
        currObj = Property.objects.filter(fullAddress=fullAddress)
        newProperty = Property(fullAddress=fullAddress, postcode=postcode)
        if not currObj:
            print('seeding')
            newProperty.save()
        else:
            newProperty = currObj[0]

        # Create reveiws for eeach property from the data...
        # MOST IMPORTANT PART OF SEEDING MAKE REPRODUCABLE!!!!!
        # Every empty ell becomes a None
        # for i in range(63):
        #     if row[i].isnan():
        #         print("cleaning")
        #         row[i] = None
        # CHANEE EMPTY FEILDS TO None... to be savec correctly....

        newReview = Review(
            verified=1,
            property=newProperty,
            reviewDate=parse_datetime(row[0]),
            timeStamp=row[0],
            livingConfirmation=row[3],
            # CHECK TYPES here...
            moveIn=row[8],
            moveOut=row[9],
            bedroomNumber=row[10],
            employmentStatus=row[11],
            reviewerName=row[12],
            buildingQuality=row[13],
            buildigComment=row[14],
            moveInHygene=row[15],
            moveInHygeneComment=row[16],
            utilities=row[17],
            utilitiesComment=row[18],
            bedroomQuality=row[19],
            bedroomQualityComment=row[20],
            furnishings=row[21],
            furnishingsComment=row[22],
            manageResponsivenes=row[23],
            manageResponsivenesComment=row[24],
            repairQuality=row[25],
            repairQualityComment=row[26],
            hiddenExpenses=row[27],
            wantedToKnowBefore=row[28],
            rentMonthly=int(float(row[29])),
            rentGoodDeal=row[30],
            neighbourhoodDescription=row[31],
            neighbourhoodSafety=row[32],
            neighbourhoodSafetyComment=row[33],
            neighbourhoodEnjoyment=row[34],
            goodPlaceForFriends=row[35],
            goodPlaceForDinnerParties=row[36],
            enjoyedCooking=row[37],
            feltLikeAHome=row[38],
            cosyInWinter=row[39],
            windowView=row[40],
            neighboursRelationship=row[41],
            study=row[42],
            easyToSleepAtNight=row[43],
            feltSafe=row[44],
            landlordRelationship=row[45],
            hotShower=row[46],
            likedMost=row[47],
            likedLeast=row[48],
            overallRating=row[49],
            dataConsent=row[50],
            contactWhenDataPublic=row[51],
            futuePaidWork=row[52],
            email=row[53],
            ambassadorPotential=row[54],
            whoSentSurvey=row[55],
            maintenanceMoveIn=row[56],
            whiteGoods=row[57],
            qualityComments=row[58],
            landlordRating=row[59],
            landlordComments=row[60],
            areaBenefits=row[61],
            areaPerks=row[62],
            wouldRecommendProperty=row[63],
        )

        newReview.save()


stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        checkout_session = stripe.PaymentIntent.create(
            amount=5000,
            currency='usd',
        )
        return JsonResponse({
            'client_secret': checkout_session['client_secret']
        })
