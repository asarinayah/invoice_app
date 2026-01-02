# invoices/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('company/', views.create_company, name='create_company'),
    path('company/create/',views.company_list,name='company_list'),
    
  
    

]
