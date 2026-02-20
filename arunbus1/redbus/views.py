from django.shortcuts import render,redirect
from decimal import Decimal
from django.http import HttpResponse, HttpResponseRedirect
from .models import User,Bus,Book


# Create your views here.
def home(request):
         return render(request, 'myapp/home.html')

def about(request):
         return render(request,'myapp/about.html')

def contact(request):
         return render(request,'myapp/contact.html')

def findbus(request):
         context={}
         if request.method=='POST':
                  source_r=request.POST.get('source')
                  dest_r=request.POST.get('destination')
                  date_r=request.POST.get('date')
                  bus_list=Bus.objects.filter(source=source_r,dest=dest_r,date=date_r)
                  if bus_list:
                           return render(request,'myapp/list.html',locals())
                  else:
                           context["error"]="Sorry no bus available"
                           return render(request,'myapp/findbus.html',context)
         else:
                  return render(request,'myapp/findbus.html')
def bookings(request):
         context={}
         if request.method=='POST':
                  id_r=request.POST.get('bus_id')
                  seats_r=int(request.POST.get('no_seats'))
                  bus=Bus.objects.get(id=id_r)
                  if bus:
                           if bus.rem >= int(seats_r):
                                    name_r=bus.bus_name
                                    cost=int(seats_r)*bus.price
                                    source_r=bus.source
                                    dest_r=bus.dest
                                    nos_r=Decimal(bus.nos)
                                    price_r=bus.price
                                    time_r=bus.time
                                    date_r=bus.date
                                    # Removed user authentication check for booking
                                    username_r = 'Guest' # Default to Guest
                                    email_r = 'guest@example.com' # Default email
                                    userid_r = 0 # Default user ID
                                    rem_r=bus.rem-seats_r
                                    Bus.objects.filter(id=id_r).update(rem=rem_r)
                                    book=Book.objects.create(name=username_r,email=email_r,
                                                             userid=userid_r,bus_name=name_r,
                                                             source=source_r,busid=id_r,
                                                             dest=dest_r,price=price_r,nos=seats_r,
                                                             date=date_r,time=time_r,status='BOOKED')
                                    print('book id',book.id)
                                    return render(request,'myapp/bookings.html',locals())
                           else:
                                    context["error"]="Sorry select fewer seats"
                                    return render(request,'myapp/findbus.html',context)
                  else:
                           return render(request,'myapp/findbus.html',context)
         else:
                  return render(request,'myapp/findbus.html')
def cancellings(request):
         context={}
         if request.method=='POST':
                  id_r=request.POST.get('bus_id')
                  try:
                           book=Book.objects.get(id=id_r)
                           bus=Bus.objects.get(id=book.busid)
                           rem_r=bus.rem + book.nos
                           Bus.objects.filter(id=book.busid).update(rem=rem_r)
                           Book.objects.filter(id=id_r).update(status='CANCELLED')
                           Book.objects.filter(id=id_r).update(nos=0)
                           return redirect('seebookings')
                  except Book.DoesNotExist:
                           context["error"]="Sorry you have not booked that bus"
                           return render(request,'myapp/error.html',context)
         else:
                  return render(request,'myapp/findbus.html',context)
def seebookings(request):
    book_list = Book.objects.all()
    if book_list:
        return render(request, 'myapp/booklist.html', locals())
    else:
        context = {"error": "Sorry no bus booked"}
        return render(request, 'myapp/findbus.html', context)

