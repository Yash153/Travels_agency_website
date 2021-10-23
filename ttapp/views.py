from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from random import randrange
from django.contrib import messages


from ttproject.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import CancelModel_Charter, CancelModel_Packages, ProfileModel, BookModel_MumbaiDarshan, BookModel_Shirdi, OrderModel_52seater, DateBetweenModel_52seater, OrderModel_17seater, DateBetweenModel_17seater, BookModel_AshtavinayakDarshan
import datetime
import json
from datetime import date
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ttproject import settings
from django.views.generic import View
from django.core.mail import EmailMultiAlternatives

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os

import razorpay
razorpay_client = razorpay.Client(auth=(settings.razorpay_id, settings.razorpay_account_id))

def signup(request):
    if request.method == 'POST':
        fn = request.POST.get('fn')
        ln = request.POST.get('ln')
        un = request.POST.get('un')
        mo = request.POST.get('mo')
        em = request.POST.get('em')
        try:
            usr = User.objects.get(username = un)
            return render(request, 'signup.html',{'msg': 'Username Already Exists'})
        except User.DoesNotExist:
            try:
                usr = User.objects.get(email=em)
                return render(request, 'signup.html',
                              {'msg': 'Email Already Exists'})
            except User.DoesNotExist:
                text = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
                pw = ''
                for i in range(4):
                    pw = pw + text[randrange(len(text))]
                print(pw)
                send_mail('Welcome to our website', 'Your password is : '+ pw, EMAIL_HOST_USER, [em])
                usr = User.objects.create_user(username = un, password = pw, email = em, first_name = fn, last_name = ln)
                p = ProfileModel(phone_num = mo, user = usr)
                p.save()
                usr.save()
                return redirect('login')
    else:
        return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pw = request.POST.get('pw')
        usr = authenticate(username=un, password=pw)
        if usr is None:
            return render(request, 'signup.html',{'msg': 'Invalid Credentials'})
        else:
            auth_login(request, usr)
            return redirect('book')
    else:
        return render(request, 'login.html')


def resetpassword(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        em = request.POST.get('em')
        try:
            usr = User.objects.get(username=un) and User.objects.get(email = em)
            text = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
            pw = ''
            for i in range(4):
                pw = pw + text[randrange(len(text))]
            print(pw)
            send_mail('Welcome to ttapp', 'Your password is : '+ pw, EMAIL_HOST_USER, [em])
            usr.set_password(pw)
            usr.save()
            return redirect('login')
        except User.DoesNotExist:
            return render(request, 'resetpassword.html',
                          {'msg': 'Invalid Credentials'})
    else:
        return render(request, 'resetpassword.html')

@login_required(login_url='/login/')
def changepassword(request):
    if request.method == 'POST':
        u1 = request.user.username
        print(u1)
        pw1 = request.POST.get('pw1')
        pw2 = request.POST.get('pw2')
        if pw1 == pw2:
            usr = User.objects.get(username=u1)
            usr.set_password(pw1)
            usr.save()
            return redirect('login')
    else:
        return render(request, 'changepassword.html')


def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required(login_url='/login/')
def book(request):
    data = ProfileModel.objects.filter(user = request.user)
    return render(request, 'book.html', {'data' : data})

@login_required(login_url='/login/')
def buscharter(request):
    data = ProfileModel.objects.filter(user = request.user)
    return render(request, 'buscharter.html', {'data' : data})

@login_required(login_url='/login/')
def actualbooking_mumbaidarshan(request):

# Getting booked date from OrderModel

    booked_date = BookModel_MumbaiDarshan.objects.all()
    db = list()
    if booked_date != None:
        for d in booked_date:
            db.append(datetime.datetime.strptime(str(d.date_booked), '%Y-%m-%d').strftime('%#d-%#m-%Y'))
        # print(db)
        

    if request.method == 'POST':
        p = "Mumbai Darshan"
        b = request.POST.get('slct2')
        n = request.POST.get('nop')
        d = request.POST.get('datepicker1')
        a = (float)(request.POST.get('total'))
        pm = request.POST.get('payment')
        print(pm)
    
        da = datetime.datetime.strptime(str(d), '%m/%d/%Y').strftime('%#d-%#m-%Y')
        d = datetime.datetime.strptime(d, '%m/%d/%Y').strftime('%Y-%#m-%#d')

        user_phone_number = ProfileModel.objects.filter(user = request.user).values('phone_num')[0]['phone_num']
        # print(pn)

        sa = BookModel_MumbaiDarshan.objects.filter(date_booked = d).values('seats_available').order_by('-dt');
        # print(sa) # List oof date selected
        # print(type(sa)) #Queryset
        if sa.exists():
            sa = sa[0]['seats_available']
            saa = sa
            print(sa)
            sa = sa - (int)(n);
            print(sa)
        else:
            sa = 52 - (int)(n);

        if sa < 0:
            return render(request, 'actualbooking_mumbaidarshan.html', { 'msg': "Only " + str(saa) +" seats are available for booking on "+str(da)  });

        if pm == 'offline':
            d1 = BookModel_MumbaiDarshan.objects.create(user = request.user, package = p, boarding_point = b, number_of_passengers = n, date_booked = d, amount = a, seats_available = sa, payment_mode = pm)
            d1.save() 
            em = request.user.email
            # message = 'Package: ' + d1.package + '\nBoarding Point: ' + d1.boarding_point +  '\nSeats Booked: ' + d1.number_of_passengers +  '\nDate of travel: ' + d1.date_booked  + '\nDate Booked: ' + str(d1.dt) + '\nPayment: Pending\nPayment Mode: Offline' 
            # send_mail('Recent order details', message, EMAIL_HOST_USER, [em])
            template = get_template('invoice.html')
            unique_id_str = str(d1.unique_id)
            data = {
                'order_id': unique_id_str,
                'transaction_id': d1.razorpay_payment_id,
                'user_email': request.user.email,
                'date': str(d1.dt),
                'name': str(d1.user.first_name)+" "+str(d1.user.last_name),
                'order': d1,
                'amount': d1.amount,
                'payment': d1.get_payment_status_display(),
            }
            html  = template.render(data)
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
            pdf = result.getvalue()
            filename = 'Invoice_' + data['order_id'] + '.pdf'
            
            mail_subject = 'Recent Booking Details'
            context_dict = {
                'user': d1.user,
                'order': d1,
                'user_phone_number': user_phone_number,
                'payment': d1.get_payment_status_display(),
            }
            template = get_template('emailinvoice.html')
            message  = template.render(context_dict)
            to_email = d1.user.email
            # for including css(only inline css works) in mail and remove autoescape off
            email = EmailMultiAlternatives(
                mail_subject,
                "hello",       # necessary to pass some message here
                settings.EMAIL_HOST_USER,
                [to_email, "yashash315.ys@gmail.com"]
            )
            email.attach_alternative(message, "text/html")
            email.attach(filename, pdf, 'application/pdf')
            email.send(fail_silently=False)   
            return render(request, 'actualbooking_mumbaidarshan.html', { 'msg': 'Booked Successfully',  'seats_available' : sa })
        else:
            order = BookModel_MumbaiDarshan.objects.create(user = request.user, package = p, boarding_point = b, number_of_passengers = n, date_booked = d, amount = a, seats_available = sa, payment_mode = pm)
            order.save()
            print(order.dt)

            
            # data = OrderModel.objects.filter(user = request.user).values('source')[0]['source']


            # data = OrderModel.objects.filter(user = request.user).values('unique_id').order_by('-dt')
            # data = data[0]['unique_id']
            # print(data)
            
            # json_db = json.dumps(db)
            order_currency = 'INR'

            callback_url = 'http://'+ str(get_current_site(request))+"/handlerequest/"
            print(callback_url)
            # notes = {'order-type': "basic order from the website", 'key':'value'}
            unique_id_str = str(order.unique_id)
            razorpay_order = razorpay_client.order.create(dict(amount=a*100, currency=order_currency, receipt=unique_id_str, payment_capture='0'))
            # print(razorpay_order)
            print(razorpay_order['id'])
            order.razorpay_order_id = razorpay_order['id']
            order.save()
            
            return render(request, 'confirm_order_MD.html', {'order':order, 'order_id': razorpay_order['id'], 'orderId':order.unique_id, 'final_price':a, 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url, 'pn' : user_phone_number})
            # return render(request, 'actualbooking_mumbaidarshan.html', { 'msg' : 'Booked Successfully', 'seats_available' : sa})
    else:
        # json_db = json.dumps(db)
        return render(request, 'actualbooking_mumbaidarshan.html')


@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        user_phone_number = ProfileModel.objects.filter(user = request.user).values('phone_num')[0]['phone_num']
        
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            # print(payment_id)
            order_id = request.POST.get('razorpay_order_id','')
            order_db = BookModel_MumbaiDarshan.objects.get(razorpay_order_id=order_id)
            unique_id_str = str(order_db.unique_id)
            
            signature = request.POST.get('razorpay_signature','')
            # print(signature)
            params_dict = { 
            'razorpay_order_id': order_id, 
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            }
            try:
                order_db = BookModel_MumbaiDarshan.objects.get(razorpay_order_id=order_id)
                print(order_db)
            except:
                return HttpResponse("505 Not Found of order_db")
            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            order_db.save()
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            print(result)
            if result==None:
                amount = order_db.amount * 100   #we have to pass in paisa
                try:
                    # razorpay_client.payment.capture(payment_id, amount)
                    # print(razorpay_client.payment.capture(payment_id, amount))
                    order_db.payment_status = 1
                    order_db.save()

                    template = get_template('invoice.html')
                    data = {
                        'order_id': unique_id_str,
                        'transaction_id': order_db.razorpay_payment_id,
                        'user_email': request.user.email,
                        'date': str(order_db.dt),
                        'name': str(order_db.user.first_name)+" "+str(order_db.user.last_name),
                        'order': order_db,
                        'amount': order_db.amount,
                        'payment': order_db.get_payment_status_display(),
                    }
                    html  = template.render(data)
                    result = BytesIO()
                    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
                    pdf = result.getvalue()
                    filename = 'Invoice_' + data['order_id'] + '.pdf'

                    mail_subject = 'Recent Booking Details'
                    # message = render_to_string('firstapp/payment/emailinvoice.html', {
                    #     'user': order_db.user,
                    #     'order': order_db
                    # })
                    context_dict = {
                        'user': order_db.user,
                        'order': order_db,
                        'user_phone_number': user_phone_number,
                        'payment': order_db.get_payment_status_display(),
                    }
                    template = get_template('emailinvoice.html')
                    message  = template.render(context_dict)
                    to_email = order_db.user.email
                    # email = EmailMessage(
                    #     mail_subject,
                    #     message, 
                    #     settings.EMAIL_HOST_USER,
                    #     [to_email]
                    # )

                    # for including css(only inline css works) in mail and remove autoescape off
                    email = EmailMultiAlternatives(
                        mail_subject,
                        "hello",       # necessary to pass some message here
                        settings.EMAIL_HOST_USER,
                        [to_email, "yashash315.ys@gmail.com"]
                    )
                    email.attach_alternative(message, "text/html")
                    email.attach(filename, pdf, 'application/pdf')
                    email.send(fail_silently=False)                    

                    return render(request, 'paymentsuccess.html',{'id':order_db.id})
                except Exception as e:
                    order_db.payment_status = 2
                    order_db.save()
                    return render(request, 'paymentfailed.html',{'msg' : str(e)})
            else:
                order_db.payment_status = 2
                order_db.save()
                return render(request, 'paymentfailed.html')
        except:
            return HttpResponse("505 not found of first try ")




class GenerateInvoice(View):
    def get(self, request, pk, *args, **kwargs):
        
        try:
            order_db = BookModel_MumbaiDarshan.objects.get(id = pk, user = request.user)     #you can filter using order_id as well
            unique_id_str = str(order_db.unique_id)
        except Exception as e:
            return HttpResponse("505 Not Found GI"+str(e))
        data = {
            'order_id': unique_id_str,
            'transaction_id': order_db.razorpay_payment_id,
            'user_email': order_db.user.email,
            'date': str(order_db.dt),
            'name': str(order_db.user.first_name) + " " + str(order_db.user.last_name),
            'order': order_db,
            'amount': order_db.amount,
            'payment': order_db.get_payment_status_display(),
        }
        pdf = render_to_pdf('invoice.html', data)
        #return HttpResponse(pdf, content_type='application/pdf')

        # force download
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %(data['order_id'])
            content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")



@login_required(login_url='/login/')
def actualbooking_shirdi(request):

# Getting booked date from OrderModel

    booked_date = BookModel_Shirdi.objects.all()
    db = list()
    if booked_date != None:
        for d in booked_date:
            db.append(datetime.datetime.strptime(str(d.date_booked), '%Y-%m-%d').strftime('%#d-%#m-%Y'))
        # print(db)
        

    if request.method == 'POST':
        p = "Shirdi"
        b = request.POST.get('slct2')
        n = request.POST.get('nop')
        d = request.POST.get('datepicker1')
        a = (float)(request.POST.get('total'))
        pm = request.POST.get('payment')
        print(pm)
    
        da = datetime.datetime.strptime(str(d), '%m/%d/%Y').strftime('%#d-%#m-%Y')
        d = datetime.datetime.strptime(d, '%m/%d/%Y').strftime('%Y-%#m-%#d')

        user_phone_number = ProfileModel.objects.filter(user = request.user).values('phone_num')[0]['phone_num']
        # print(pn)

        sa = BookModel_Shirdi.objects.filter(date_booked = d).values('seats_available').order_by('-dt');
        # print(sa) # List oof date selected
        # print(type(sa)) #Queryset
        if sa.exists():
            sa = sa[0]['seats_available']
            saa = sa
            print(sa)
            sa = sa - (int)(n);
            print(sa)
        else:
            sa = 52 - (int)(n);

        if sa < 0:
            return render(request, 'actualbooking_shirdi.html', { 'msg': "Only " + str(saa) +" seats are available for booking on "+str(da)  });

        if pm == 'offline':
            d1 = BookModel_Shirdi.objects.create(user = request.user, package = p, boarding_point = b, number_of_passengers = n, date_booked = d, amount = a, seats_available = sa, payment_mode = pm)
            d1.save() 
            template = get_template('invoice.html')
            unique_id_str = str(d1.unique_id)
            data = {
                'order_id': unique_id_str,
                'transaction_id': d1.razorpay_payment_id,
                'user_email': request.user.email,
                'date': str(d1.dt),
                'name': str(d1.user.first_name)+" "+str(d1.user.last_name),
                'order': d1,
                'amount': d1.amount,
                'payment': d1.get_payment_status_display(),
            }
            html  = template.render(data)
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
            pdf = result.getvalue()
            filename = 'Invoice_' + data['order_id'] + '.pdf'

            mail_subject = 'Recent Booking Details'
            context_dict = {
                'user': d1.user,
                'order': d1,
                'user_phone_number': user_phone_number,
                'payment': d1.get_payment_status_display(),
            }
            template = get_template('emailinvoice.html')
            message  = template.render(context_dict)
            to_email = d1.user.email
            # for including css(only inline css works) in mail and remove autoescape off
            email = EmailMultiAlternatives(
                mail_subject,
                "hello",       # necessary to pass some message here
                settings.EMAIL_HOST_USER,
                [to_email, "yashash315.ys@gmail.com"]
            )
            email.attach_alternative(message, "text/html")
            email.attach(filename, pdf, 'application/pdf')
            email.send(fail_silently=False)   
            return render(request, 'actualbooking_shirdi.html', { 'msg': 'Booked Successfully',  'seats_available' : sa })
        else:
            order = BookModel_Shirdi.objects.create(user = request.user, package = p, boarding_point = b, number_of_passengers = n, date_booked = d, amount = a, seats_available = sa, payment_mode = pm)
            order.save()
            print(order.dt)

            
            # data = OrderModel.objects.filter(user = request.user).values('source')[0]['source']


            # data = OrderModel.objects.filter(user = request.user).values('unique_id').order_by('-dt')
            # data = data[0]['unique_id']
            # print(data)
            
            # json_db = json.dumps(db)
            order_currency = 'INR'

            callback_url = 'http://'+ str(get_current_site(request))+"/handlerequest_shirdi/"
            print(callback_url)
            # notes = {'order-type': "basic order from the website", 'key':'value'}
            unique_id_str = str(order.unique_id)
            razorpay_order = razorpay_client.order.create(dict(amount=a*100, currency=order_currency, receipt=unique_id_str, payment_capture='0'))
            # print(razorpay_order)
            print(razorpay_order['id'])
            order.razorpay_order_id = razorpay_order['id']
            order.save()
            
            return render(request, 'confirm_order_MD.html', {'order':order, 'order_id': razorpay_order['id'], 'orderId':order.unique_id, 'final_price':a, 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url, 'pn' : user_phone_number})
    else:
        # json_db = json.dumps(db)
        return render(request, 'actualbooking_shirdi.html')

@csrf_exempt
def handlerequest_shirdi(request):
    if request.method == "POST":
        user_phone_number = ProfileModel.objects.filter(user = request.user).values('phone_num')[0]['phone_num']
        
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            # print(payment_id)
            order_id = request.POST.get('razorpay_order_id','')
            order_db = BookModel_Shirdi.objects.get(razorpay_order_id=order_id)
            unique_id_str = str(order_db.unique_id)
            
            signature = request.POST.get('razorpay_signature','')
            # print(signature)
            params_dict = { 
            'razorpay_order_id': order_id, 
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            }
            try:
                order_db = BookModel_Shirdi.objects.get(razorpay_order_id=order_id)
                print(order_db)
            except:
                return HttpResponse("505 Not Found of order_db")
            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            order_db.save()
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            print(result)
            if result==None:
                amount = order_db.amount * 100   #we have to pass in paisa
                try:
                    # razorpay_client.payment.capture(payment_id, amount)
                    # print(razorpay_client.payment.capture(payment_id, amount))
                    order_db.payment_status = 1
                    order_db.save()

                    template = get_template('invoice.html')
                    data = {
                        'order_id': unique_id_str,
                        'transaction_id': order_db.razorpay_payment_id,
                        'user_email': request.user.email,
                        'date': str(order_db.dt),
                        'name': str(order_db.user.first_name)+" "+str(order_db.user.last_name),
                        'order': order_db,
                        'amount': order_db.amount,
                        'payment': order_db.get_payment_status_display(),
                    }
                    html  = template.render(data)
                    result = BytesIO()
                    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
                    pdf = result.getvalue()
                    filename = 'Invoice_' + data['order_id'] + '.pdf'

                    mail_subject = 'Recent Booking Details'
                    # message = render_to_string('firstapp/payment/emailinvoice.html', {
                    #     'user': order_db.user,
                    #     'order': order_db
                    # })
                    context_dict = {
                        'user': order_db.user,
                        'order': order_db,
                        'user_phone_number': user_phone_number,
                        'payment': order_db.get_payment_status_display(),
                    }
                    template = get_template('emailinvoice.html')
                    message  = template.render(context_dict)
                    to_email = order_db.user.email
                    # email = EmailMessage(
                    #     mail_subject,
                    #     message, 
                    #     settings.EMAIL_HOST_USER,
                    #     [to_email]
                    # )

                    # for including css(only inline css works) in mail and remove autoescape off
                    email = EmailMultiAlternatives(
                        mail_subject,
                        "hello",       # necessary to pass some message here
                        settings.EMAIL_HOST_USER,
                        [to_email, "yashash315.ys@gmail.com"]
                    )
                    email.attach_alternative(message, "text/html")
                    email.attach(filename, pdf, 'application/pdf')
                    email.send(fail_silently=False)                    

                    return render(request, 'paymentsuccess_shirdi.html',{'id':order_db.id})
                except Exception as e:
                    order_db.payment_status = 2
                    order_db.save()
                    return render(request, 'paymentfailed.html',{'msg' : str(e)})
            else:
                order_db.payment_status = 2
                order_db.save()
                return render(request, 'paymentfailed.html')
        except:
            return HttpResponse("505 not found of first try ")

class GenerateInvoice_shirdi(View):
    def get(self, request, pk, *args, **kwargs):
        
        try:
            order_db = BookModel_Shirdi.objects.get(id = pk, user = request.user)     #you can filter using order_id as well
            unique_id_str = str(order_db.unique_id)
        except Exception as e:
            return HttpResponse("505 Not Found"+str(e))
        data = {
            'order_id': unique_id_str,
            'transaction_id': order_db.razorpay_payment_id,
            'user_email': order_db.user.email,
            'date': str(order_db.dt),
            'name': str(order_db.user.first_name) + " " + str(order_db.user.last_name),
            'order': order_db,
            'amount': order_db.amount,
            'payment': order_db.get_payment_status_display(),
        }
        pdf = render_to_pdf('invoice.html', data)
        #return HttpResponse(pdf, content_type='application/pdf')

        # force download
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %(data['order_id'])
            content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")



@login_required(login_url='/login/')
def actualbooking_ashtavinayakdarshan(request):

# Getting booked date from OrderModel

    booked_date = BookModel_AshtavinayakDarshan.objects.all()
    db = list()
    if booked_date != None:
        for d in booked_date:
            db.append(datetime.datetime.strptime(str(d.date_booked), '%Y-%m-%d').strftime('%#d-%#m-%Y'))
        # print(db)
        

    if request.method == 'POST':
        p = "Ashtavinayak Darshan"
        b = request.POST.get('slct2')
        n = request.POST.get('nop')
        d = request.POST.get('datepicker1')
        a = (float)(request.POST.get('total'))
        pm = request.POST.get('payment')
        print(pm)
    
        da = datetime.datetime.strptime(str(d), '%m/%d/%Y').strftime('%#d-%#m-%Y')
        d = datetime.datetime.strptime(d, '%m/%d/%Y').strftime('%Y-%#m-%#d')

        user_phone_number = ProfileModel.objects.filter(user = request.user).values('phone_num')[0]['phone_num']
        # print(pn)

        sa = BookModel_AshtavinayakDarshan.objects.filter(date_booked = d).values('seats_available').order_by('-dt');
        # print(sa) # List oof date selected
        # print(type(sa)) #Queryset
        if sa.exists():
            sa = sa[0]['seats_available']
            saa = sa
            print(sa)
            sa = sa - (int)(n);
            print(sa)
        else:
            sa = 17 - (int)(n);

        if sa < 0:
            return render(request, 'actualbooking_ashtavinayakdarshan.html', { 'msg': "Only " + str(saa) +" seats are available for booking on "+str(da)  });

        if pm == 'offline':
            d1 = BookModel_AshtavinayakDarshan.objects.create(user = request.user, package = p, boarding_point = b, number_of_passengers = n, date_booked = d, amount = a, seats_available = sa, payment_mode = pm)
            d1.save() 

            template = get_template('invoice.html')
            unique_id_str = str(d1.unique_id)
            data = {
                'order_id': unique_id_str,
                'transaction_id': d1.razorpay_payment_id,
                'user_email': request.user.email,
                'date': str(d1.dt),
                'name': str(d1.user.first_name)+" "+str(d1.user.last_name),
                'order': d1,
                'amount': d1.amount,
                'payment': d1.get_payment_status_display(),
            }
            html  = template.render(data)
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
            pdf = result.getvalue()
            filename = 'Invoice_' + data['order_id'] + '.pdf'

            mail_subject = 'Recent Booking Details'
            context_dict = {
                'user': d1.user,
                'order': d1,
                'user_phone_number': user_phone_number,
                'payment': d1.get_payment_status_display(),
            }
            template = get_template('emailinvoice.html')
            message  = template.render(context_dict)
            to_email = d1.user.email
            # for including css(only inline css works) in mail and remove autoescape off
            email = EmailMultiAlternatives(
                mail_subject,
                "hello",       # necessary to pass some message here
                settings.EMAIL_HOST_USER,
                [to_email, "yashash315.ys@gmail.com"]
            )
            email.attach_alternative(message, "text/html")
            email.attach(filename, pdf, 'application/pdf')
            email.send(fail_silently=False)   
            return render(request, 'actualbooking_ashtavinayakdarshan.html', { 'msg': 'Booked Successfully',  'seats_available' : sa })
        else:
            order = BookModel_AshtavinayakDarshan.objects.create(user = request.user, package = p, boarding_point = b, number_of_passengers = n, date_booked = d, amount = a, seats_available = sa, payment_mode = pm)
            order.save()
            print(order.dt)

            
            # data = OrderModel.objects.filter(user = request.user).values('source')[0]['source']


            # data = OrderModel.objects.filter(user = request.user).values('unique_id').order_by('-dt')
            # data = data[0]['unique_id']
            # print(data)
            
            # json_db = json.dumps(db)
            order_currency = 'INR'

            callback_url = 'http://'+ str(get_current_site(request))+"/handlerequest_ashtavinayakdarshan/"
            print(callback_url)
            # notes = {'order-type': "basic order from the website", 'key':'value'}
            unique_id_str = str(order.unique_id)
            razorpay_order = razorpay_client.order.create(dict(amount=a*100, currency=order_currency, receipt=unique_id_str, payment_capture='0'))
            # print(razorpay_order)
            print(razorpay_order['id'])
            order.razorpay_order_id = razorpay_order['id']
            order.save()
            
            return render(request, 'confirm_order_MD.html', {'order':order, 'order_id': razorpay_order['id'], 'orderId':order.unique_id, 'final_price':a, 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url, 'pn' : user_phone_number})
    else:
        # json_db = json.dumps(db)
        return render(request, 'actualbooking_ashtavinayakdarshan.html')

@csrf_exempt
def handlerequest_ashtavinayakdarshan(request):
    if request.method == "POST":
        user_phone_number = ProfileModel.objects.filter(user = request.user).values('phone_num')[0]['phone_num']
        
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            # print(payment_id)
            order_id = request.POST.get('razorpay_order_id','')
            order_db = BookModel_AshtavinayakDarshan.objects.get(razorpay_order_id=order_id)
            unique_id_str = str(order_db.unique_id)
            
            signature = request.POST.get('razorpay_signature','')
            # print(signature)
            params_dict = { 
            'razorpay_order_id': order_id, 
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            }
            try:
                order_db = BookModel_AshtavinayakDarshan.objects.get(razorpay_order_id=order_id)
                print(order_db)
            except:
                return HttpResponse("505 Not Found of order_db")
            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            order_db.save()
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            print(result)
            if result==None:
                amount = order_db.amount * 100   #we have to pass in paisa
                try:
                    # razorpay_client.payment.capture(payment_id, amount)
                    # print(razorpay_client.payment.capture(payment_id, amount))
                    order_db.payment_status = 1
                    order_db.save()

                    template = get_template('invoice.html')
                    data = {
                        'order_id': unique_id_str,
                        'transaction_id': order_db.razorpay_payment_id,
                        'user_email': request.user.email,
                        'date': str(order_db.dt),
                        'name': str(order_db.user.first_name)+" "+str(order_db.user.last_name),
                        'order': order_db,
                        'amount': order_db.amount,
                        'payment': order_db.get_payment_status_display(),
                    }
                    html  = template.render(data)
                    result = BytesIO()
                    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
                    pdf = result.getvalue()
                    filename = 'Invoice_' + data['order_id'] + '.pdf'

                    mail_subject = 'Recent Booking Details'
                    # message = render_to_string('firstapp/payment/emailinvoice.html', {
                    #     'user': order_db.user,
                    #     'order': order_db
                    # })
                    context_dict = {
                        'user': order_db.user,
                        'order': order_db,
                        'user_phone_number': user_phone_number,
                        'payment': order_db.get_payment_status_display(),
                    }
                    template = get_template('emailinvoice.html')
                    message  = template.render(context_dict)
                    to_email = order_db.user.email
                    # email = EmailMessage(
                    #     mail_subject,
                    #     message, 
                    #     settings.EMAIL_HOST_USER,
                    #     [to_email]
                    # )

                    # for including css(only inline css works) in mail and remove autoescape off
                    email = EmailMultiAlternatives(
                        mail_subject,
                        "hello",       # necessary to pass some message here
                        settings.EMAIL_HOST_USER,
                        [to_email, "yashash315.ys@gmail.com"]
                    )
                    email.attach_alternative(message, "text/html")
                    email.attach(filename, pdf, 'application/pdf')
                    email.send(fail_silently=False)                    

                    return render(request, 'paymentsuccess_ashtavinayakdarshan.html',{'id':order_db.id})
                except Exception as e:
                    order_db.payment_status = 2
                    order_db.save()
                    return render(request, 'paymentfailed.html',{'msg' : str(e)})
            else:
                order_db.payment_status = 2
                order_db.save()
                return render(request, 'paymentfailed.html')
        except:
            return HttpResponse("505 not found of first try ")

class GenerateInvoice_ashtavinayakdarshan(View):
    def get(self, request, pk, *args, **kwargs):
        
        try:
            order_db = BookModel_AshtavinayakDarshan.objects.get(id = pk, user = request.user)     #you can filter using order_id as well
            unique_id_str = str(order_db.unique_id)
        except Exception as e:
            return HttpResponse("505 Not Found"+str(e))
        data = {
            'order_id': unique_id_str,
            'transaction_id': order_db.razorpay_payment_id,
            'user_email': order_db.user.email,
            'date': str(order_db.dt),
            'name': str(order_db.user.first_name) + " " + str(order_db.user.last_name),
            'order': order_db,
            'amount': order_db.amount,
            'payment': order_db.get_payment_status_display(),
        }
        pdf = render_to_pdf('invoice.html', data)
        #return HttpResponse(pdf, content_type='application/pdf')

        # force download
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %(data['order_id'])
            content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


@login_required(login_url='/login/')
def actualcharter_52seater(request):
    date_between_data = DateBetweenModel_52seater.objects.all()
    booked_date = OrderModel_52seater.objects.all()
    db_between = list()
    db = list()
    dr = list()
    if booked_date != None:
        for d in booked_date:
            db.append(datetime.datetime.strptime(str(d.date_booked), '%Y-%m-%d').strftime('%#d-%#m-%Y'))
            dr.append(datetime.datetime.strptime(str(d.date_released), '%Y-%m-%d').strftime('%#d-%#m-%Y'))
        db.extend(dr)
        print(db)
    if date_between_data != None:
        for d in date_between_data:
            db_between.append(datetime.datetime.strptime(str(d.date_between), '%Y-%m-%d').strftime('%#d-%#m-%Y'))
        db.extend(db_between)
        print(db)

    if request.method == 'POST':
        s = request.POST.get('origin')
        d = request.POST.get('destination')
        f = request.POST.get('datepicker1')
        t = request.POST.get('datepicker2')
        try:
            amt = (float)(request.POST.get('amount'))
        except: 
            messages.error(request,'Please select source and destination from suggested places')
            return redirect('actualcharter_52seater')
        c = request.POST.get('category')
        a = request.POST.get('additional_info')
        pm = request.POST.get('payment')
        user_phone_number = ProfileModel.objects.filter(user = request.user).values('phone_num')[0]['phone_num']
        # print(f) #dd/mm/yyyy
        # print(t)

        # print(type(f))
        # print(type(t)) # str

        f_date_object = datetime.datetime.strptime(f, '%d/%m/%Y')
        print("*******************")
        print(f_date_object)
        print(type(f_date_object))

        t_date_object = datetime.datetime.strptime(t, '%d/%m/%Y')
        print(t_date_object)
        print(type(t_date_object))
        f = datetime.datetime.strptime(f, '%d/%m/%Y').strftime('%Y-%#m-%#d')
        t = datetime.datetime.strptime(t, '%d/%m/%Y').strftime('%Y-%#m-%#d')

        # f_date_object = datetime.datetime.strptime(f, '%Y-%m-%d')
        # t_date_object = datetime.datetime.strptime(t, '%Y-%m-%d')

        # print(type(f_date_object))

        from_date = datetime.datetime.strptime(f, '%Y-%m-%d').strftime('%d')
        from_month = datetime.datetime.strptime(f, '%Y-%m-%d').strftime('%m')
        from_year = datetime.datetime.strptime(f, '%Y-%m-%d').strftime('%Y')
        print(from_date)
        print(from_month)
        print(from_year)

        to_date = datetime.datetime.strptime(t, '%Y-%m-%d').strftime('%d')
        to_month = datetime.datetime.strptime(t, '%Y-%m-%d').strftime('%m')
        to_year = datetime.datetime.strptime(t, '%Y-%m-%d').strftime('%Y')
        print(to_date)
        print(to_month)
        print(to_year)

        print(type(f))
        print(type(t))

        if(t_date_object<f_date_object):
            json_db = json.dumps(db)
            json_db_between = json.dumps(db_between)
            return render(request, 'actualcharter_52seater.html', { 'db' : json_db, 'db_between' : json_db_between, 'msg' : "Please enter valid dates" })
        else:

            total_days = t_date_object - f_date_object
            print(total_days.days)
            total_days_bus_reserved = total_days.days + 1
            no_days_to_be_disabled = total_days.days - 1

            if(no_days_to_be_disabled > 0):
                date_temp = datetime.datetime.strptime(f, '%Y-%m-%d')
                print(date_temp)
                # 
                # print(new_date_temp)
                for i in range(no_days_to_be_disabled):
                    j = i + 1
                    new_date_temp = date_temp + datetime.timedelta(days=j)
                    print(new_date_temp)
                    date_between_saving_format = datetime.datetime.strptime(str(new_date_temp), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                    date_between = datetime.datetime.strptime(str(new_date_temp), '%Y-%m-%d %H:%M:%S').strftime('%#d-%#m-%Y')
                    print(date_between)
                    d2 = DateBetweenModel_52seater(user = request.user, date_between = date_between_saving_format)
                    d2.save()
                    # db_between.append(datetime.datetime.strptime(str(new_date_temp), '%Y-%m-%d %H:%M:%S').strftime('%#d-%#m-%Y'))
                # print(db)
                # print(db_between)


            # d1 = OrderModel_52seater(user = request.user, source = s, destination = d, date_booked = f, date_released = t, amount = amt)
            # d1.save()

            
            json_db = json.dumps(db)
            json_db_between = json.dumps(db_between)
            # return render(request, 'actualcharter_52seater.html', { 'msg' : 'Booked Successfully', 'db' : json_db, 'db_between' : json_db_between})


            if pm == 'offline':
                d1 = OrderModel_52seater.objects.create(user = request.user, source = s, destination = d, date_booked = f, date_released = t, amount = amt, total_days_bus_reserved = total_days_bus_reserved, no_days_to_be_disabled = no_days_to_be_disabled, payment_mode = pm)
                d1.save() 
                em = request.user.email
                # message = 'Package: ' + d1.package + '\nBoarding Point: ' + d1.boarding_point +  '\nSeats Booked: ' + d1.number_of_passengers +  '\nDate of travel: ' + d1.date_booked  + '\nDate Booked: ' + str(d1.dt) + '\nPayment: Pending\nPayment Mode: Offline' 
                # send_mail('Recent order details', message, EMAIL_HOST_USER, [em])
                template = get_template('invoice_charter.html')
                unique_id_str = str(d1.unique_id)
                data = {
                    'order_id': unique_id_str,
                    'transaction_id': d1.razorpay_payment_id,
                    'user_email': request.user.email,
                    'date': str(d1.dt),
                    'name': str(d1.user.first_name)+" "+str(d1.user.last_name),
                    'order': d1,
                    'amount': d1.amount,
                    'payment': d1.get_payment_status_display(),
                }
                html  = template.render(data)
                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
                pdf = result.getvalue()
                filename = 'Invoice_' + data['order_id'] + '.pdf'

                mail_subject = 'Recent Booking Details'
                context_dict = {
                    'user': d1.user,
                    'user_phone_number': user_phone_number,
                    'order': d1,
                    'payment': d1.get_payment_status_display(),
                }
                template = get_template('emailinvoice_charter.html')
                message  = template.render(context_dict)
                to_email = d1.user.email
                # for including css(only inline css works) in mail and remove autoescape off
                email = EmailMultiAlternatives(
                    mail_subject,
                    "hello",       # necessary to pass some message here
                    settings.EMAIL_HOST_USER,
                    [to_email, "yashash315.ys@gmail.com"]
                )
                email.attach_alternative(message, "text/html")
                email.attach(filename, pdf, 'application/pdf')
                email.send(fail_silently=False)   
                
                return render(request, 'actualcharter_52seater.html', { 'msg': 'Booked Successfully', 'db' : json_db, 'db_between' : json_db_between})
            else:
                order = OrderModel_52seater.objects.create(user = request.user, source = s, destination = d, date_booked = f, date_released = t, amount = amt, total_days_bus_reserved = total_days_bus_reserved, no_days_to_be_disabled = no_days_to_be_disabled, payment_mode = pm)
                order.save()
                print(order.dt)

                
                # data = OrderModel.objects.filter(user = request.user).values('source')[0]['source']


                # data = OrderModel.objects.filter(user = request.user).values('unique_id').order_by('-dt')
                # data = data[0]['unique_id']
                # print(data)
                
                # json_db = json.dumps(db)
                order_currency = 'INR'

                callback_url = 'http://'+ str(get_current_site(request))+"/handlerequest_52seater/"
                print(callback_url)
                # notes = {'order-type': "basic order from the website", 'key':'value'}
                unique_id_str = str(order.unique_id)
                razorpay_order = razorpay_client.order.create(dict(amount=amt*100, currency=order_currency, receipt=unique_id_str, payment_capture='0'))
                # print(razorpay_order)
                print(razorpay_order['id'])
                order.razorpay_order_id = razorpay_order['id']
                order.save()
                
                return render(request, 'confirm_order_52seater.html', {'order':order, 'order_id': razorpay_order['id'], 'orderId':order.unique_id, 'final_price':amt, 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url, 'pn' : user_phone_number})
    else:
        json_db = json.dumps(db)
        json_db_between = json.dumps(db_between)
        return render(request, 'actualcharter_52seater.html', { 'db' : json_db, 'db_between' : json_db_between })

@csrf_exempt
def handlerequest_52seater(request):
    if request.method == "POST":
        user_phone_number = ProfileModel.objects.filter(user = request.user).values('phone_num')[0]['phone_num']
        
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            # print(payment_id)
            order_id = request.POST.get('razorpay_order_id','')
            order_db = OrderModel_52seater.objects.get(razorpay_order_id=order_id)
            unique_id_str = str(order_db.unique_id)
            
            signature = request.POST.get('razorpay_signature','')
            # print(signature)
            params_dict = { 
            'razorpay_order_id': order_id, 
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            }
            try:
                order_db = OrderModel_52seater.objects.get(razorpay_order_id=order_id)
                print(order_db)
            except:
                return HttpResponse("505 Not Found of order_db")
            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            order_db.save()
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            print(result)
            if result==None:
                amount = order_db.amount * 100   #we have to pass in paisa
                try:
                    # razorpay_client.payment.capture(payment_id, amount)
                    # print(razorpay_client.payment.capture(payment_id, amount))
                    order_db.payment_status = 1
                    order_db.save()

                    template = get_template('invoice_charter.html')
                    data = {
                        'order_id': unique_id_str,
                        'transaction_id': order_db.razorpay_payment_id,
                        'user_email': request.user.email,
                        'date': str(order_db.dt),
                        'name': str(order_db.user.first_name)+" "+str(order_db.user.last_name),
                        'order': order_db,
                        'amount': order_db.amount,
                        'payment': order_db.get_payment_status_display(),
                    }
                    html  = template.render(data)
                    result = BytesIO()
                    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
                    pdf = result.getvalue()
                    filename = 'Invoice_' + data['order_id'] + '.pdf'

                    mail_subject = 'Recent Booking Details'
                    # message = render_to_string('firstapp/payment/emailinvoice.html', {
                    #     'user': order_db.user,
                    #     'order': order_db
                    # })
                    context_dict = {
                        'user': order_db.user,
                        'order': order_db,
                        'user_phone_number': user_phone_number,
                        'payment': order_db.get_payment_status_display(),
                    }
                    template = get_template('emailinvoice.html')
                    message  = template.render(context_dict)
                    to_email = order_db.user.email
                    # email = EmailMessage(
                    #     mail_subject,
                    #     message, 
                    #     settings.EMAIL_HOST_USER,
                    #     [to_email]
                    # )

                    # for including css(only inline css works) in mail and remove autoescape off
                    email = EmailMultiAlternatives(
                        mail_subject,
                        "hello",       # necessary to pass some message here
                        settings.EMAIL_HOST_USER,
                        [to_email, "yashash315.ys@gmail.com"]
                    )
                    email.attach_alternative(message, "text/html")
                    email.attach(filename, pdf, 'application/pdf')
                    email.send(fail_silently=False)                    

                    return render(request, 'paymentsuccess_52seater.html',{'id':order_db.id})
                except Exception as e:
                    order_db.payment_status = 2
                    order_db.save()
                    return render(request, 'paymentfailed.html',{'msg' : "in creation of pdf" + str(e)})
            else:
                order_db.payment_status = 2
                order_db.save()
                return render(request, 'paymentfailed.html')
        except:
            return HttpResponse("505 not found of first try ")




class GenerateInvoice_52seater(View):
    def get(self, request, pk, *args, **kwargs):
        
        try:
            order_db = OrderModel_52seater.objects.get(id = pk, user = request.user)     #you can filter using order_id as well
            unique_id_str = str(order_db.unique_id)
        except Exception as e:
            return HttpResponse("505 Not Found GI"+str(e))
        data = {
            'order_id': unique_id_str,
            'transaction_id': order_db.razorpay_payment_id,
            'user_email': order_db.user.email,
            'date': str(order_db.dt),
            'name': str(order_db.user.first_name) + " " + str(order_db.user.last_name),
            'order': order_db,
            'amount': order_db.amount,
            'payment': order_db.get_payment_status_display(),
        }
        pdf = render_to_pdf('invoice_charter.html', data)
        #return HttpResponse(pdf, content_type='application/pdf')

        # force download
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %(data['order_id'])
            content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")



@login_required(login_url='/login/')
def actualcharter_17seater(request):
    date_between_data = DateBetweenModel_17seater.objects.all()
    booked_date = OrderModel_17seater.objects.all()
    db_between = list()
    db = list()
    dr = list()
    if booked_date != None:
        for d in booked_date:
            db.append(datetime.datetime.strptime(str(d.date_booked), '%Y-%m-%d').strftime('%#d-%#m-%Y'))
            dr.append(datetime.datetime.strptime(str(d.date_released), '%Y-%m-%d').strftime('%#d-%#m-%Y'))
        db.extend(dr)
        print(db)
    if date_between_data != None:
        for d in date_between_data:
            db_between.append(datetime.datetime.strptime(str(d.date_between), '%Y-%m-%d').strftime('%#d-%#m-%Y'))
        db.extend(db_between)
        print(db)

    if request.method == 'POST':
        s = request.POST.get('origin')
        d = request.POST.get('destination')
        f = request.POST.get('datepicker1')
        t = request.POST.get('datepicker2')
        amt = (float)(request.POST.get('amount'))
        c = request.POST.get('category')
        a = request.POST.get('additional_info')
        pm = request.POST.get('payment')
        user_phone_number = ProfileModel.objects.filter(user = request.user).values('phone_num')[0]['phone_num']
        # print(f) #dd/mm/yyyy
        # print(t)

        # print(type(f))
        # print(type(t)) # str

        f_date_object = datetime.datetime.strptime(f, '%d/%m/%Y')
        print(f_date_object)
        print(type(f_date_object))

        t_date_object = datetime.datetime.strptime(t, '%d/%m/%Y')
        print(t_date_object)
        print(type(t_date_object))

        f = datetime.datetime.strptime(f, '%d/%m/%Y').strftime('%Y-%#m-%#d')
        t = datetime.datetime.strptime(t, '%d/%m/%Y').strftime('%Y-%#m-%#d')

        # f_date_object = datetime.datetime.strptime(f, '%Y-%m-%d')
        # t_date_object = datetime.datetime.strptime(t, '%Y-%m-%d')

        # print(type(f_date_object))

        from_date = datetime.datetime.strptime(f, '%Y-%m-%d').strftime('%d')
        from_month = datetime.datetime.strptime(f, '%Y-%m-%d').strftime('%m')
        from_year = datetime.datetime.strptime(f, '%Y-%m-%d').strftime('%Y')
        print(from_date)
        print(from_month)
        print(from_year)

        to_date = datetime.datetime.strptime(t, '%Y-%m-%d').strftime('%d')
        to_month = datetime.datetime.strptime(t, '%Y-%m-%d').strftime('%m')
        to_year = datetime.datetime.strptime(t, '%Y-%m-%d').strftime('%Y')
        print(to_date)
        print(to_month)
        print(to_year)

        print(type(f))
        print(type(t))

        if(t_date_object<f_date_object):
            json_db = json.dumps(db)
            json_db_between = json.dumps(db_between)
            return render(request, 'actualcharter_17seater.html', { 'db' : json_db, 'db_between' : json_db_between, 'msg' : "Please enter valid dates" })
        else:

            total_days = t_date_object - f_date_object
            print(total_days.days)
            total_days_bus_reserved = total_days.days + 1
            no_days_to_be_disabled = total_days.days - 1

            if(no_days_to_be_disabled > 0):
                date_temp = datetime.datetime.strptime(f, '%Y-%m-%d')
                print(date_temp)
                # 
                # print(new_date_temp)
                for i in range(no_days_to_be_disabled):
                    j = i + 1
                    new_date_temp = date_temp + datetime.timedelta(days=j)
                    print(new_date_temp)
                    date_between_saving_format = datetime.datetime.strptime(str(new_date_temp), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                    date_between = datetime.datetime.strptime(str(new_date_temp), '%Y-%m-%d %H:%M:%S').strftime('%#d-%#m-%Y')
                    print(date_between)
                    d2 = DateBetweenModel_17seater(user = request.user, date_between = date_between_saving_format)
                    d2.save()
                    # db_between.append(datetime.datetime.strptime(str(new_date_temp), '%Y-%m-%d %H:%M:%S').strftime('%#d-%#m-%Y'))
                # print(db)
                # print(db_between)


            # d1 = OrderModel_52seater(user = request.user, source = s, destination = d, date_booked = f, date_released = t, amount = amt)
            # d1.save()

            
            json_db = json.dumps(db)
            json_db_between = json.dumps(db_between)
            # return render(request, 'actualcharter_52seater.html', { 'msg' : 'Booked Successfully', 'db' : json_db, 'db_between' : json_db_between})


            if pm == 'offline':
                d1 = OrderModel_17seater.objects.create(user = request.user, source = s, destination = d, date_booked = f, date_released = t, amount = amt, total_days_bus_reserved = total_days_bus_reserved, no_days_to_be_disabled = no_days_to_be_disabled, payment_mode = pm)
                d1.save() 
                em = request.user.email
                # message = 'Package: ' + d1.package + '\nBoarding Point: ' + d1.boarding_point +  '\nSeats Booked: ' + d1.number_of_passengers +  '\nDate of travel: ' + d1.date_booked  + '\nDate Booked: ' + str(d1.dt) + '\nPayment: Pending\nPayment Mode: Offline' 
                # send_mail('Recent order details', message, EMAIL_HOST_USER, [em])
                template = get_template('invoice_charter.html')
                unique_id_str = str(d1.unique_id)
                data = {
                    'order_id': unique_id_str,
                    'transaction_id': d1.razorpay_payment_id,
                    'user_email': request.user.email,
                    'date': str(d1.dt),
                    'name': str(d1.user.first_name)+" "+str(d1.user.last_name),
                    'order': d1,
                    'amount': d1.amount,
                    'payment': d1.get_payment_status_display(),
                }
                html  = template.render(data)
                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
                pdf = result.getvalue()
                filename = 'Invoice_' + data['order_id'] + '.pdf'

                mail_subject = 'Recent Booking Details'
                context_dict = {
                    'user': d1.user,
                    'order': d1,
                    'user_phone_number': user_phone_number,
                    'payment': d1.get_payment_status_display(),
                }
                template = get_template('emailinvoice_charter.html')
                message  = template.render(context_dict)
                to_email = d1.user.email
                # for including css(only inline css works) in mail and remove autoescape off
                email = EmailMultiAlternatives(
                    mail_subject,
                    "hello",       # necessary to pass some message here
                    settings.EMAIL_HOST_USER,
                    [to_email, "yashash315.ys@gmail.com"]
                )
                email.attach_alternative(message, "text/html")
                email.attach(filename, pdf, 'application/pdf')
                email.send(fail_silently=False)   
                
                return render(request, 'actualcharter_17seater.html', { 'msg': 'Booked Successfully', 'db' : json_db, 'db_between' : json_db_between})
            else:
                order = OrderModel_17seater.objects.create(user = request.user, source = s, destination = d, date_booked = f, date_released = t, amount = amt, total_days_bus_reserved = total_days_bus_reserved, no_days_to_be_disabled = no_days_to_be_disabled, payment_mode = pm)
                order.save()
                print(order.dt)

                
                # data = OrderModel.objects.filter(user = request.user).values('source')[0]['source']


                # data = OrderModel.objects.filter(user = request.user).values('unique_id').order_by('-dt')
                # data = data[0]['unique_id']
                # print(data)
                
                # json_db = json.dumps(db)
                order_currency = 'INR'

                callback_url = 'http://'+ str(get_current_site(request))+"/handlerequest_17seater/"
                print(callback_url)
                # notes = {'order-type': "basic order from the website", 'key':'value'}
                unique_id_str = str(order.unique_id)
                razorpay_order = razorpay_client.order.create(dict(amount=amt*100, currency=order_currency, receipt=unique_id_str, payment_capture='0'))
                # print(razorpay_order)
                print(razorpay_order['id'])
                order.razorpay_order_id = razorpay_order['id']
                order.save()
                
                return render(request, 'confirm_order_52seater.html', {'order':order, 'order_id': razorpay_order['id'], 'orderId':order.unique_id, 'final_price':amt, 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url, 'pn' : user_phone_number})
    else:
        json_db = json.dumps(db)
        json_db_between = json.dumps(db_between)
        return render(request, 'actualcharter_17seater.html', { 'db' : json_db, 'db_between' : json_db_between })

@csrf_exempt
def handlerequest_17seater(request):
    if request.method == "POST":
        user_phone_number = ProfileModel.objects.filter(user = request.user).values('phone_num')[0]['phone_num']
        
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            # print(payment_id)
            order_id = request.POST.get('razorpay_order_id','')
            order_db = OrderModel_17seater.objects.get(razorpay_order_id=order_id)
            unique_id_str = str(order_db.unique_id)
            
            signature = request.POST.get('razorpay_signature','')
            # print(signature)
            params_dict = { 
            'razorpay_order_id': order_id, 
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            }
            try:
                order_db = OrderModel_17seater.objects.get(razorpay_order_id=order_id)
                print(order_db)
            except:
                return HttpResponse("505 Not Found of order_db")
            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            order_db.save()
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            print(result)
            if result==None:
                amount = order_db.amount * 100   #we have to pass in paisa
                try:
                    # razorpay_client.payment.capture(payment_id, amount)
                    # print(razorpay_client.payment.capture(payment_id, amount))
                    order_db.payment_status = 1
                    order_db.save()

                    template = get_template('invoice_charter.html')
                    data = {
                        'order_id': unique_id_str,
                        'transaction_id': order_db.razorpay_payment_id,
                        'user_email': request.user.email,
                        'date': str(order_db.dt),
                        'name': str(order_db.user.first_name)+" "+str(order_db.user.last_name),
                        'order': order_db,
                        'amount': order_db.amount,
                        'payment': order_db.get_payment_status_display(),
                    }
                    html  = template.render(data)
                    result = BytesIO()
                    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
                    pdf = result.getvalue()
                    filename = 'Invoice_' + data['order_id'] + '.pdf'

                    mail_subject = 'Recent Booking Details'
                    # message = render_to_string('firstapp/payment/emailinvoice.html', {
                    #     'user': order_db.user,
                    #     'order': order_db
                    # })
                    context_dict = {
                        'user': order_db.user,
                        'order': order_db,
                        'user_phone_number': user_phone_number,
                        'payment': order_db.get_payment_status_display(),
                    }
                    template = get_template('emailinvoice.html')
                    message  = template.render(context_dict)
                    to_email = order_db.user.email
                    # email = EmailMessage(
                    #     mail_subject,
                    #     message, 
                    #     settings.EMAIL_HOST_USER,
                    #     [to_email]
                    # )

                    # for including css(only inline css works) in mail and remove autoescape off
                    email = EmailMultiAlternatives(
                        mail_subject,
                        "hello",       # necessary to pass some message here
                        settings.EMAIL_HOST_USER,
                        [to_email, "yashash315.ys@gmail.com"]
                    )
                    email.attach_alternative(message, "text/html")
                    email.attach(filename, pdf, 'application/pdf')
                    email.send(fail_silently=False)                    

                    return render(request, 'paymentsuccess_17seater.html',{'id':order_db.id})
                except Exception as e:
                    order_db.payment_status = 2
                    order_db.save()
                    return render(request, 'paymentfailed.html',{'msg' : "in creation of pdf" + str(e)})
            else:
                order_db.payment_status = 2
                order_db.save()
                return render(request, 'paymentfailed.html')
        except:
            return HttpResponse("505 not found of first try ")




class GenerateInvoice_17seater(View):
    def get(self, request, pk, *args, **kwargs):
        
        try:
            order_db = OrderModel_17seater.objects.get(id = pk, user = request.user)     #you can filter using order_id as well
            unique_id_str = str(order_db.unique_id)
        except Exception as e:
            return HttpResponse("505 Not Found GI"+str(e))
        data = {
            'order_id': unique_id_str,
            'transaction_id': order_db.razorpay_payment_id,
            'user_email': order_db.user.email,
            'date': str(order_db.dt),
            'name': str(order_db.user.first_name) + " " + str(order_db.user.last_name),
            'order': order_db,
            'amount': order_db.amount,
            'payment': order_db.get_payment_status_display(),
        }
        pdf = render_to_pdf('invoice_charter.html', data)
        #return HttpResponse(pdf, content_type='application/pdf')

        # force download
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %(data['order_id'])
            content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


@login_required(login_url='/login/')
def orderhistory(request):
    charter_history = OrderModel_52seater.objects.filter(user=request.user).order_by('-dt');
    print(charter_history)
    charter_history1 = OrderModel_17seater.objects.filter(user=request.user).order_by('-dt');

    package_history = BookModel_MumbaiDarshan.objects.filter(user=request.user).order_by('-dt');
    package_history1 = BookModel_Shirdi.objects.filter(user=request.user).order_by('-dt');
    package_history2 = BookModel_AshtavinayakDarshan.objects.filter(user=request.user).order_by('-dt');

    cancelcharter_history = CancelModel_Charter.objects.filter(user=request.user).order_by('-dt')
    cancelpackages_history = CancelModel_Packages.objects.filter(user = request.user).order_by('-dt')

    return render(request, 'orderhistory.html', { 'charter_history' : charter_history, 'charter_history1' : charter_history1, 'package_history2' : package_history2, 'package_history1' : package_history1, 'package_history' : package_history, 'cancelcharter_history': cancelcharter_history, 'cancelpackages_history': cancelpackages_history })


def fetch_resources(uri, rel):
    path = os.path.join(uri.replace(settings.STATIC_URL, ""))
    return path

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def cancelbooking(request,site,pk):
    print(site)
    print(pk)
    if site == "cancelbooking_52seater":
        try:
            order_db = OrderModel_52seater.objects.get(id = pk, user = request.user)     #you can filter using order_id as well
            unique_id_str = str(order_db.unique_id)
            order_db_date_between = DateBetweenModel_52seater.objects.filter(user = request.user)
        except Exception as e:
            return HttpResponse("505 Not Found GI"+str(e))

        order_db.booking_status = 2;
        order_db.save()

        c1 = CancelModel_Charter.objects.create(user=request.user, unique_id = order_db.unique_id, date_time_booked = order_db.dt, source = order_db.source, destination = order_db.destination, date_booked = order_db.date_booked, date_released = order_db.date_released, amount = order_db.amount, payment_mode = order_db.payment_mode, total_days_bus_reserved = order_db.total_days_bus_reserved,no_days_to_be_disabled = order_db.no_days_to_be_disabled,payment_status = order_db.payment_status, razorpay_order_id = order_db.razorpay_order_id, razorpay_payment_id = order_db.razorpay_payment_id, razorpay_signature = order_db.razorpay_signature)
        c1.save()

        date_enable_from = OrderModel_52seater.objects.filter(id = pk).values('date_booked')[0]['date_booked']
        user_phone_number = ProfileModel.objects.filter(user = request.user).values('phone_num')[0]['phone_num']
        print(date_enable_from)
        date_enable_to = OrderModel_52seater.objects.filter(id = pk).values('date_released')[0]['date_released']
        print(date_enable_to)
        total_reserved_date_enable = order_db.total_days_bus_reserved

        t = date_enable_to - date_enable_from
        print(t)

        f = datetime.datetime.strptime(str(date_enable_from), '%Y-%m-%d').strftime('%d/%m/%Y')
        t = datetime.datetime.strptime(str(date_enable_to), '%Y-%m-%d').strftime('%d/%m/%Y')
        

        date_enable_from_date_object = datetime.datetime.strptime(f, '%d/%m/%Y')
        date_enable_to_date_object = datetime.datetime.strptime(t, '%d/%m/%Y')
        print(date_enable_to_date_object)

        total_days = date_enable_to_date_object - date_enable_from_date_object
        print("&&&&&&&&&&&&&&&&")
        print(total_days)
        no_of_days_between = 1

        date_between = datetime.datetime.strptime(str(date_enable_from), '%Y-%m-%d')
        print(date_between)


        no_days_to_be_disabled = OrderModel_52seater.objects.filter(id = pk).values('no_days_to_be_disabled')[0]['no_days_to_be_disabled']

        if no_days_to_be_disabled <= 0:
            d1 = OrderModel_52seater.objects.get(date_booked = date_enable_from)
            d2 = OrderModel_52seater.objects.get(date_released = date_enable_to)
            d1.delete()
            d2.delete()
            # OrderModel_52seater.save()
        elif no_days_to_be_disabled > 0:
            d1 = OrderModel_52seater.objects.get(date_booked = date_enable_from)
            d2 = OrderModel_52seater.objects.get(date_released = date_enable_to)
            d1.delete()
            d2.delete()
            while(date_between < date_enable_to_date_object):
                for i in range(no_days_to_be_disabled):
                    # j = i + 1 WRONG

                    date_between = date_between + datetime.timedelta(days=1)
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print(date_between)
                    try:#jaise hi d3 waala line exception dega uske pehle ke sab dates delete hogaye honge to sidha orderhistory pe redirect kar
                        d3 = DateBetweenModel_52seater.objects.filter(date_between = date_between).values('date_between')[0]['date_between']
                        print(d3)
                        
                        d4 = DateBetweenModel_52seater.objects.get(date_between = d3)
                        d4.delete()
                    except:
                        return redirect(orderhistory)
        return redirect(orderhistory)


        
    elif site == "cancelbooking_17seater":
        try:
            order_db = OrderModel_17seater.objects.get(id = pk, user = request.user)     #you can filter using order_id as well
            unique_id_str = str(order_db.unique_id)
            order_db_date_between = DateBetweenModel_17seater.objects.filter(user = request.user)
        except Exception as e:
            return HttpResponse("505 Not Found GI"+str(e))

        order_db.booking_status = 2;
        order_db.save()

        c1 = CancelModel_Charter.objects.create(user=request.user, unique_id = order_db.unique_id, date_time_booked = order_db.dt, source = order_db.source, destination = order_db.destination, date_booked = order_db.date_booked, date_released = order_db.date_released, amount = order_db.amount, payment_mode = order_db.payment_mode, total_days_bus_reserved = order_db.total_days_bus_reserved,no_days_to_be_disabled = order_db.no_days_to_be_disabled,payment_status = order_db.payment_status, razorpay_order_id = order_db.razorpay_order_id, razorpay_payment_id = order_db.razorpay_payment_id, razorpay_signature = order_db.razorpay_signature)
        c1.save()

        

        date_enable_from = OrderModel_17seater.objects.filter(id = pk).values('date_booked')[0]['date_booked']
        user_phone_number = ProfileModel.objects.filter(user = request.user).values('phone_num')[0]['phone_num']
        print(date_enable_from)
        date_enable_to = OrderModel_17seater.objects.filter(id = pk).values('date_released')[0]['date_released']
        print(date_enable_to)

        date_between = datetime.datetime.strptime(str(date_enable_from), '%Y-%m-%d')

        t = datetime.datetime.strptime(str(date_enable_to), '%Y-%m-%d').strftime('%d/%m/%Y')
        date_enable_to_date_object = datetime.datetime.strptime(t, '%d/%m/%Y')

        no_days_to_be_disabled = OrderModel_17seater.objects.filter(id = pk).values('no_days_to_be_disabled')[0]['no_days_to_be_disabled']

        if no_days_to_be_disabled <= 0:
            d1 = OrderModel_17seater.objects.get(date_booked = date_enable_from)
            d2 = OrderModel_17seater.objects.get(date_released = date_enable_to)
            d1.delete()
            d2.delete()
            # OrderModel_52seater.save()
        elif no_days_to_be_disabled > 0:
            d1 = OrderModel_17seater.objects.get(date_booked = date_enable_from)
            d2 = OrderModel_17seater.objects.get(date_released = date_enable_to)
            d1.delete()
            d2.delete()
            while(date_between < date_enable_to_date_object):
                for i in range(no_days_to_be_disabled):
                    # j = i + 1 WRONG

                    date_between = date_between + datetime.timedelta(days=1)
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print(date_between)
                    try:#jaise hi d3 waala line exception dega uske pehle ke sab dates delete hogaye honge to sidha orderhistory pe redirect kar
                        d3 = DateBetweenModel_17seater.objects.filter(date_between = date_between).values('date_between')[0]['date_between']
                        print(d3)
                        
                        d4 = DateBetweenModel_17seater.objects.get(date_between = d3)
                        d4.delete()
                    except:
                        return redirect(orderhistory)
        return redirect(orderhistory)
        
    elif site == "cancelbooking_mumbaidarshan":
        try:
            order_db = BookModel_MumbaiDarshan.objects.get(id = pk, user = request.user)     #you can filter using order_id as well
        except Exception as e:
            return HttpResponse("505 Not Found GI"+str(e))

        order_db.booking_status = 2;
        order_db.save()
      
        c1 = CancelModel_Packages.objects.create(user=request.user, unique_id = order_db.unique_id, package = order_db.package, date_time_booked = order_db.dt, boarding_point = order_db.boarding_point, number_of_passengers = order_db.number_of_passengers, date_booked = order_db.date_booked, amount = order_db.amount, seats_available = order_db.seats_available, payment_mode = order_db.payment_mode, payment_status = order_db.payment_status, razorpay_order_id = order_db.razorpay_order_id, razorpay_payment_id = order_db.razorpay_payment_id, razorpay_signature = order_db.razorpay_signature)
        c1.save()

        seats_to_be_inserted = order_db.number_of_passengers
        print(seats_to_be_inserted)
        # d = BookModel_MumbaiDarshan.objects.filter(id = pk, user = request.user).values('date_booked').order_by('-dt');
        update_row = BookModel_MumbaiDarshan.objects.get(id = pk, user = request.user)
        print(update_row.seats_available)
        update_row.seats_available += seats_to_be_inserted
        update_row.save()
        print(update_row.seats_available)
        update_row.delete()
        return redirect(orderhistory)

    elif site == "cancelbooking_shirdi":
        try:
            order_db = BookModel_Shirdi.objects.get(id = pk, user = request.user)     #you can filter using order_id as well
        except Exception as e:
            return HttpResponse("505 Not Found GI"+str(e))
        
        order_db.booking_status = 2;
        order_db.save()

        c1 = CancelModel_Packages.objects.create(user=request.user, unique_id = order_db.unique_id, package = order_db.package, boarding_point = order_db.boarding_point, date_time_booked = order_db.dt, number_of_passengers = order_db.number_of_passengers, date_booked = order_db.date_booked, amount = order_db.amount, seats_available = order_db.seats_available, payment_mode = order_db.payment_mode, payment_status = order_db.payment_status, razorpay_order_id = order_db.razorpay_order_id, razorpay_payment_id = order_db.razorpay_payment_id, razorpay_signature = order_db.razorpay_signature)
        c1.save()

        seats_to_be_inserted = order_db.number_of_passengers
        print(seats_to_be_inserted)
        # d = BookModel_MumbaiDarshan.objects.filter(id = pk, user = request.user).values('date_booked').order_by('-dt');
        update_row = BookModel_Shirdi.objects.get(id = pk, user = request.user)
        print(update_row.seats_available)
        update_row.seats_available += seats_to_be_inserted
        update_row.save()
        print(update_row.seats_available)
        update_row.delete()
        return redirect(orderhistory)

    elif site == "cancelbooking_ashtavinayakdarshan":
        try:
            order_db = BookModel_AshtavinayakDarshan.objects.get(id = pk, user = request.user)     #you can filter using order_id as well
        except Exception as e:
            return HttpResponse("505 Not Found GI"+str(e))
        
        order_db.booking_status = 2;
        order_db.save()

        c1 = CancelModel_Packages.objects.create(user=request.user, unique_id = order_db.unique_id, package = order_db.package,date_time_booked = order_db.dt, boarding_point = order_db.boarding_point, number_of_passengers = order_db.number_of_passengers, date_booked = order_db.date_booked, amount = order_db.amount, seats_available = order_db.seats_available, payment_mode = order_db.payment_mode, payment_status = order_db.payment_status, razorpay_order_id = order_db.razorpay_order_id, razorpay_payment_id = order_db.razorpay_payment_id, razorpay_signature = order_db.razorpay_signature)
        c1.save()

        seats_to_be_inserted = order_db.number_of_passengers
        print(seats_to_be_inserted)
        # d = BookModel_MumbaiDarshan.objects.filter(id = pk, user = request.user).values('date_booked').order_by('-dt');
        update_row = BookModel_AshtavinayakDarshan.objects.get(id = pk, user = request.user)
        print(update_row.seats_available)
        update_row.seats_available += seats_to_be_inserted
        update_row.save()
        print(update_row.seats_available)
        update_row.delete()
        return redirect(orderhistory)
    return render(request, 'orderhistory.html')


def pendingpayment(request, site, pk):
    print(site)
    print(pk)
    if site == "mumbaidarshan":
        order = BookModel_MumbaiDarshan.objects.get(id = pk)
        order.payment_mode = "online"
        a = order.amount
        print(order.dt)
        user_phone_number = ProfileModel.objects.filter(user = request.user).values('phone_num')[0]['phone_num']

        order_currency = 'INR'

        callback_url = 'http://'+ str(get_current_site(request))+"/handlerequest/"
        print(callback_url)
        unique_id_str = str(order.unique_id)
        razorpay_order = razorpay_client.order.create(dict(amount=a*100, currency=order_currency, receipt=unique_id_str, payment_capture='0'))
        print(razorpay_order['id'])
        order.razorpay_order_id = razorpay_order['id']
        order.save()
            
        return render(request, 'confirm_order_MD.html', {'order':order, 'order_id': razorpay_order['id'], 'orderId':order.unique_id, 'final_price':a, 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url, 'pn' : user_phone_number})
        
    elif site == "shirdi":
        order = BookModel_Shirdi.objects.get(id = pk)
        order.payment_mode = "online"
        a = order.amount
        print(order.dt)
        user_phone_number = ProfileModel.objects.filter(user = request.user).values('phone_num')[0]['phone_num']

        order_currency = 'INR'

        callback_url = 'http://'+ str(get_current_site(request))+"/handlerequest_shirdi/"
        print(callback_url)
        unique_id_str = str(order.unique_id)
        razorpay_order = razorpay_client.order.create(dict(amount=a*100, currency=order_currency, receipt=unique_id_str, payment_capture='0'))
        print(razorpay_order['id'])
        order.razorpay_order_id = razorpay_order['id']
        order.save()
            
        return render(request, 'confirm_order_MD.html', {'order':order, 'order_id': razorpay_order['id'], 'orderId':order.unique_id, 'final_price':a, 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url, 'pn' : user_phone_number})
    elif site == "ashtavinayakdarshan":
        order = BookModel_AshtavinayakDarshan.objects.get(id = pk)
        order.payment_mode = "online"
        a = order.amount
        print(order.dt)
        user_phone_number = ProfileModel.objects.filter(user = request.user).values('phone_num')[0]['phone_num']

        order_currency = 'INR'

        callback_url = 'http://'+ str(get_current_site(request))+"/handlerequest_ashtavinayakdarshan/"
        print(callback_url)
        unique_id_str = str(order.unique_id)
        razorpay_order = razorpay_client.order.create(dict(amount=a*100, currency=order_currency, receipt=unique_id_str, payment_capture='0'))
        print(razorpay_order['id'])
        order.razorpay_order_id = razorpay_order['id']
        order.save()
            
        return render(request, 'confirm_order_MD.html', {'order':order, 'order_id': razorpay_order['id'], 'orderId':order.unique_id, 'final_price':a, 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url, 'pn' : user_phone_number})

    elif site == "52seater":
        order = OrderModel_52seater.objects.get(id = pk)
        order.payment_mode = "online"
        a = order.amount
        print(order.dt)
        user_phone_number = ProfileModel.objects.filter(user = request.user).values('phone_num')[0]['phone_num']

        order_currency = 'INR'

        callback_url = 'http://'+ str(get_current_site(request))+"/handlerequest_52seater/"
        print(callback_url)
        unique_id_str = str(order.unique_id)
        razorpay_order = razorpay_client.order.create(dict(amount=(float)(a*100), currency=order_currency, receipt=unique_id_str, payment_capture='0'))
        print(razorpay_order['id'])
        order.razorpay_order_id = razorpay_order['id']
        order.save()
        return render(request, 'confirm_order_52seater.html', {'order':order, 'order_id': razorpay_order['id'], 'orderId':order.unique_id, 'final_price':a, 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url, 'pn' : user_phone_number})

    elif site == "17seater":
        order = OrderModel_17seater.objects.get(id = pk)
        order.payment_mode = "online"
        a = order.amount
        print(order.dt)
        user_phone_number = ProfileModel.objects.filter(user = request.user).values('phone_num')[0]['phone_num']

        order_currency = 'INR'

        callback_url = 'http://'+ str(get_current_site(request))+"/handlerequest_17seater/"
        print(callback_url)
        unique_id_str = str(order.unique_id)
        razorpay_order = razorpay_client.order.create(dict(amount=(float)(a*100), currency=order_currency, receipt=unique_id_str, payment_capture='0'))
        print(razorpay_order['id'])
        order.razorpay_order_id = razorpay_order['id']
        order.save()
        return render(request, 'confirm_order_52seater.html', {'order':order, 'order_id': razorpay_order['id'], 'orderId':order.unique_id, 'final_price':a, 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url, 'pn' : user_phone_number})

def contact(request):
    return render(request, 'contact.html')