from django.urls import path
from authentication.authentication import myclassView

urlpatterns = [
   path(r'myclassView/', myclassView.as_view()) 
]