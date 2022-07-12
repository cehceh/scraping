from django.urls import path
from .views import *

# app_name = ""

urlpatterns = [
    
    path("create/excel/sheet/", create_excel, name="create_excel"),
    path("create/google/sheet/", create_google_sheet, name="create_google_sheet"),

]