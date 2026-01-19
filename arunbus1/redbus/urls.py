from django.urls import path
from . import views

urlpatterns=[
         path('',views.home,name='home'),
         path('about',views.about,name='about'),
         path('contact',views.contact,name='contact'),
         path('findbus',views.findbus,name='findbus'),
         path('bookings',views.bookings,name='bookings'),
         path('cancellings',views.cancellings,name='cancellings'),
         path('seebookings',views.seebookings,name='seebookings'),
         
         
         ]
 
