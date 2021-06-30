from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls import url
from beta.views import (
    CreateCheckoutSessionView,

)

urlpatterns = [
    path('', views.landing, name='landing'),
    path('reasult/<str:hashId>/', views.reasult, name='reasult'),
    # path('search', views.search, name='search'),
    path('searchReasult', views.searchReasult, name='searchReasult'),
    # make the link a dynamic string..
    path('review', views.review, name='review'),
    path('propertyList', views.propertyList, name='propertyList'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('accounts/', include('allauth.urls')),
    path('payment_form/', views.payment_form, name='payment_form'),
    url('payment_form/checkout', views.checkout, name="checkout_page"),
    path('aboutUs', views.aboutUs, name='aboutUs'),
    path('FormWizardView', views.FormWizardView, name='FormWizardView'),
    path('seeder', views.seeder, name='seeder'),
    path('checkout', views.checkout, name='checkout'),
    path('create-checkout-session', CreateCheckoutSessionView.as_view(),
         name='create-checkout-session')


]
