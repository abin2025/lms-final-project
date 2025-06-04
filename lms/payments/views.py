from django.shortcuts import render,redirect

# Create your views here.

from django.views import View

from course.models import Course

from . models import Payments,Transaction

from students.models import Students

import razorpay

from decouple import config

import datetime

class EnrollConfirmationView(View) :

    def get(self,request,*args,**kwargs) :

        uuid = kwargs.get('uuid')

        course = Course.objects.get(uuid=uuid)

        payment,created = Payments.objects.get_or_create(student=Students.objects.get(profile=request.user),course=course,amount=course.offer_fee if course.offer_fee else course.fee)

        data = {'payment' : payment}

        return render(request,'payments/enroll-confirmation.html',context=data)

class RazorpayView(View) :

    def get(self,request,*args,**kwargs) :

        uuid = kwargs.get('uuid')

        course = Course.objects.get(uuid=uuid)

        student = Students.objects.get(profile=request.user)

        payment = Payments.objects.get(student = student,course=course)

        transaction = Transaction.objects.create(payment=payment)

        client = razorpay.Client(auth=(config('RZP_CLIENT_ID'),config("RZP_CLIENT_SECRET")))

        data = { "amount": payment.amount*100, "currency": "INR", "receipt": "order_rcptid_11" }

        order = client.order.create(data=data) #Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise

        rzp_order_id = order.get('id')

        transaction.rzp_order_id = rzp_order_id

        transaction.save()

        data = {'client_id': config('RZP_CLIENT_ID'),'rzp_order_id': rzp_order_id,'amount': payment.amount*100}

        return render(request,'payments/payment-page.html',context=data)   


class PaymentVerifyView(View) :

    def post(self,request,*args,**kwargs) :

        rzp_order_id = request.POST.get('razorpay_order_id')

        rzp_payment_id = request.POST.get('razorpay_payment_id')

        rzp_payment_signature = request.POST.get('razorpay_signature')

        print(request.POST)

        
        client = razorpay.Client(auth=(config('RZP_CLIENT_ID'),config("RZP_CLIENT_SECRET")))

        transaction = Transaction.objects.get(rzp_order_id = rzp_order_id)

        time_now = datetime.datetime.now()

        transaction.rzp_payment_id = rzp_payment_id

        transaction.rzp_payment_signature = rzp_payment_signature

        try :


            client.utility.verify_payment_signature({
                                        'razorpay_order_id': rzp_order_id,
                                        'razorpay_payment_id': rzp_payment_id,
                                        'razorpay_signature': rzp_payment_signature
                                         })

            

            transaction.status = 'success'

            transaction.save()

            transaction.payment.status = 'success'

            transaction.payment.paid_at = time_now

            return redirect('home')


        except :

            transaction.status = 'failed'

            transaction.save()

            return redirect('razorpay-view',uuid=transaction.payment.course.uuid) 

            
            
                   
