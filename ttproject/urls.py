"""ttproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ttapp.views import login, logout, resetpassword, changepassword, signup, book, actualbooking_mumbaidarshan, buscharter, actualbooking_shirdi, actualbooking_ashtavinayakdarshan,actualcharter_52seater,actualcharter_17seater,orderhistory,handlerequest,GenerateInvoice,handlerequest_shirdi,GenerateInvoice_shirdi,handlerequest_ashtavinayakdarshan,GenerateInvoice_ashtavinayakdarshan,handlerequest_52seater,GenerateInvoice_52seater,handlerequest_17seater,GenerateInvoice_17seater, cancelbooking, pendingpayment, contact

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',login,name = 'login'),
    path('login/',login,name = 'login'),
    path('logout/',logout,name = 'logout'),
    path('resetpassword/',resetpassword,name = 'resetpassword'),
    path('changepassword/',changepassword,name = 'changepassword'),
    path('signup/',signup,name = 'signup'),
    path('book/',book,name = 'book'),
    path('actualbooking_mumbaidarshan/', actualbooking_mumbaidarshan,name = 'actualbooking_mumbaidarshan'),
    path('actualbooking_shirdi/',actualbooking_shirdi,name = 'actualbooking_shirdi'),
    path('actualbooking_ashtavinayakdarshan/', actualbooking_ashtavinayakdarshan, name = 'actualbooking_ashtavinayakdarshan'),
    path('buscharter/',buscharter,name = 'buscharter'),
    path('actualcharter_17seater/',actualcharter_17seater,name = 'actualcharter_17seater'),
    path('actualcharter_52seater/',actualcharter_52seater,name = 'actualcharter_52seater'),
    path('orderhistory/',orderhistory,name = 'orderhistory'),
    path('handlerequest/', handlerequest, name = 'handlerequest'),
    path('handlerequest_shirdi/',handlerequest_shirdi,name = 'handlerequest_shirdi'),
    path('handlerequest_ashtavinayakdarshan/', handlerequest_ashtavinayakdarshan, name = 'handlerequest_ashtavinayakdarshan'),
    path('handlerequest_52seater/', handlerequest_52seater, name = 'handlerequest_52seater'),
    path('handlerequest_17seater/', handlerequest_17seater, name = 'handlerequest_17seater'),
    path('generateinvoice/<int:pk>/', GenerateInvoice.as_view(), name = 'generateinvoice'),
    path('generateinvoice_shirdi/<int:pk>/',GenerateInvoice_shirdi.as_view(), name = 'generateinvoice_shirdi'),
    path('generateinvoice_ashtavinayakdarshan/<int:pk>/',GenerateInvoice_ashtavinayakdarshan.as_view(), name = 'generateinvoice_ashtavinayakdarshan'),
    path('generateinvoice_52seater/<int:pk>/', GenerateInvoice_52seater.as_view(), name = 'generateinvoice_52seater'),
    path('generateinvoice_17seater/<int:pk>/', GenerateInvoice_17seater.as_view(), name = 'generateinvoice_17seater'),
    path('orderhistory/generateinvoice/<int:pk>/', GenerateInvoice.as_view(), name = 'generateinvoice1'),
    path('orderhistory/generateinvoice_shirdi/<int:pk>/', GenerateInvoice_shirdi.as_view(), name = 'generateinvoice2'),
    path('orderhistory/generateinvoice_ashtavinayakdarshan/<int:pk>/', GenerateInvoice_ashtavinayakdarshan.as_view(), name = 'generateinvoice3'),
    path('orderhistory/generateinvoice_52seater/<int:pk>/', GenerateInvoice_52seater.as_view(), name = 'generateinvoice4'),
    path('orderhistory/generateinvoice_17seater/<int:pk>/', GenerateInvoice_17seater.as_view(), name = 'generateinvoice5'),
    path('orderhistory/<str:site>/<int:pk>/', cancelbooking, name = 'cancelbooking'),
    path('orderhistory/pendingpayment/<str:site>/<int:pk>', pendingpayment, name = 'pendingpayment'),
    path('contact/',contact, name='contact'),
]
