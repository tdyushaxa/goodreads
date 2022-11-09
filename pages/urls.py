from django.urls import path

from pages.views import *

urlpatterns=[
    path('',LandingViewPage.as_view(),name='landing'),
    path('home/',HomePageView.as_view(),name='home')

]