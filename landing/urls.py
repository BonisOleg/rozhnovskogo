from django.urls import path
from . import views

app_name = 'landing'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('lead/', views.LeadFormView.as_view(), name='lead'),
    path('prozorro/', views.ProzorroView.as_view(), name='prozorro'),
]
