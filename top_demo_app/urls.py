from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_us, name='contact-us'),
    path('sign_up/', views.sign_up, name='sign-up'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('otp/', views.verify_otp, name='verify-otp'),
    path('new-password/', views.new_password, name="new-password"),
    path('change-password', views.change_password, name='change-password'),
]
