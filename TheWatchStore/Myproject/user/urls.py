from django.urls import path
from . import views

urlpatterns=[
    path('',views.home),
    path('home/',views.home),
    path('about/',views.about),
    path('services/',views.services),
    path('contactus/',views.contactus),
    path('products/',views.prod),
    path('myprofile/',views.myprofile),
    path('updateprofile/',views.updateprofile),
    path('myorders/',views.myorders),
    path('signup/',views.signup),
    path('signin/',views.signin),
    path('process/',views.process),
    path('viewdetails/',views.viewdetails),
    path('logout/',views.logout),
    path('cart/',views.cart),
]