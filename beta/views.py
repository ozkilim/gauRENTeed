import stripe
from jinja2 import *
from django.shortcuts import render
from django.contrib.auth.models import User
from beta.models import Property, Review, ReviewProduct
from beta.forms import ReviewForm, CustomUserCreationForm, CustomUser
# Create your views here.
from gauRENTeed import settings
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from gauRENTeed.middleware.login_exempt import login_exempt
from beta.token import account_activation_token
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import login
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers
from django.forms.models import model_to_dict
from django.http import JsonResponse


def landing(request):

    if request.method == 'POST':
        # get the searched result and redirect to correct page here
        address = request.POST.get('property')

        return redirect('reasult', address=address)

    if 'term' in request.GET:
        qs = Property.objects.filter(
            address__istartswith=request.GET.get('term'))
        addresses = []
        for property in qs:
            addresses.append(property.address)
        return JsonResponse(addresses, safe=False)

    return render(request, 'landing.html')


def propertyList(request):
    # Get all properties in daatabase.
    properties = Property.objects.all()
    context = {'properties': properties}
    # Render the list of objects
    return render(request, 'propertyList.html', context=context)


def reasult(request, address):
    # Later will need to add hashing so users cannot get to the page for free
    property = Property.objects.get(address=address)
    # Get all properties
    # filter the get reviews for properties
    # Order the reviews by date from oldest to newest

    propertyReviews = Review.objects.filter(
        property=property).order_by('reviewDate').values()

    # propertyReviews = FooForm(data=model_to_dict(Review.objects.filter(
    #     property=property).order_by('reviewDate')))
    # unpack and rebuild the feilds to display her later on so all automated..
    print(propertyReviews)
    context = {'property': property, 'reviews': propertyReviews}

    return render(request, 'tempReasult.html', context)


def searchReasult(request):

    return render(request, 'searchReasult.html')


def review(request):
    # Get current reviews object
    reviews = Review.objects.all()
    form = ReviewForm(request.POST)

    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        # Check if the form is valid:
        print(form.errors)
        if form.is_valid():
            # Not saving the review currently to back end....
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            # book_instance.due_back = form.cleaned_data['renewal_date']
            form.save()
    context = {"form": form}

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
        return redirect('foodshow:index')
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
        model="Honda Civic",
        year=2017
    )

    if request.method == "POST":
        token = request.POST.get("stripeToken")

    try:
        charge = stripe.Charge.create(
            amount=2000,
            currency="usd",
            source=token,
            description="The product charged to the user"
        )

        review_purchased.charge_id = charge.id

    except stripe.error.CardError as ce:
        return False, ce

    else:
        review_purchased.save()
        return redirect("thank_you_page")
        # The payment was successfully processed, the user's card was charged.
        # You can now redirect the user to another page or whatever you want
