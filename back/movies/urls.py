from django.urls import path
from . import views

urlpatterns = [
    path('fundings/', views.funding_list),
    path('fundings/detail/', views.funding_detail),
]