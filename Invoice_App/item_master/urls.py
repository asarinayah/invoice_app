from django.urls import path
from . import views
urlpatterns = [
    path('create/',views.newitem),
    path('items/', views.item_list, name='item_list'),
]
