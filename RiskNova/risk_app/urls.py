from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict_form, name='predict_form'),
    path('prediction/<int:prediction_id>/', views.result, name='result'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.home, name='about'),
    path('research/', views.home, name='research'),
]
