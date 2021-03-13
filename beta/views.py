from django.shortcuts import render
from beta.models import Property, Review
from beta.forms import ReviewForm, CustomUserCreationForm, CustomUser
# Create your views here.
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from gauRENTeed.middleware.login_exempt import login_exempt
from django.contrib.auth.models import User
from beta.token import account_activation_token
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import login
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site


def landing(request):

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
    print(property)
    propertyReviews = Review.objects.filter(property=property)
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


@login_exempt
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


@login_exempt
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
