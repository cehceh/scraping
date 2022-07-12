from django.urls import path
from .views import *



urlpatterns = [
    #* url for api 
    path("", ExcelListCreateAPIView.as_view(), name="ExcelListCreateAPIView"),
    path("<int:index>/", ExcelDetailAPIView.as_view(), name="ExcelDetailAPIView"),
]

