from django.urls import path, include
from authentication.authentication import myclassView
from django.contrib import admin

urlpatterns = [
   path(r'myclassView/', myclassView.as_view()),
   #path("api/v1/", include('djoser.urls')),
   #path("api/v1/", include('djoser.urls.authtoken')),
]


    #path("api/v1/", include('djoser.urls')),
    #Setting the tokens
    #