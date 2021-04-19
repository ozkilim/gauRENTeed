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
    # Later will need to add hashing so users cannot get to the page for free
    property = Property.objects.get(hashId=hashId)
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
               'aggregateReview': aggregateReview}

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


stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):

    review_purchased = ReviewProduct(
        name="a review ",
        year="10"
    )

    if request.method == "POST":
        token = request.POST.get("stripeToken")

    try:
        charge = stripe.Charge.create(
            amount=200,
            currency="gbp",
            source=token,
            description="The product charged to the user"
        )
        review_purchased.charge_id = charge.id

    except stripe.error.CardError as ce:
        print(ce)
        return False, ce

    else:
        review_purchased.save()
        # redirect to the review that was requested
        return redirect("landing")
        # The payment was successfully processed, the user's card was charged.
        # You can now redirect the user to another page or whatever you want


class FormWizardView(SessionWizardView):
    template_name = "wizardReview"
    form_list = [ReviewForm, PropertyCreationForm]

    def done(self, form_list):
        return render(self.request, 'wizardReview.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })
