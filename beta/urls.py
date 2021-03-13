from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.landing, name='landing'),
    path('reasult/<str:address>/', views.reasult, name='reasult'),
    path('search', views.search, name='search'),
    path('searchReasult', views.searchReasult, name='searchReasult'),
    # make the link a dynamic string..
    path('review', views.review, name='review'),
    path('propertyList', views.propertyList, name='propertyList'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
