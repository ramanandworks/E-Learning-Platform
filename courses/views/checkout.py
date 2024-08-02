from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from courses.models import Course, Video,quiz_model,Payment,UserCourse
from courses import models
from codewithwasef.settings import *
import razorpay
from datetime import datetime
from time import time
from django.views.decorators.csrf import csrf_exempt

client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

def checkout(request,slug):
    course=Course.objects.get(slug=slug)
    user=None
    if not request.user.is_authenticated :
        return redirect("login")
    # if((request.user.is_authenticated is False)):
    #     return redirect("login")
    
    user=request.user
    #u enroll to watch all videos

    action=request.GET.get('action')
    order=None
    payment=None
    error=None
    if action=='create_payment':
        try:
            user_course=UserCourse.objects.get(user=user,course=course)
            error="already enrolled in this course"
        except:
            pass
        if error is None:    
            amount=int((course.price-(course.price*course.discount*0.01))*100)
            currency="INR"
            notes={
                'email':user.email,
                'name':f'{user.first_name}{user.last_name}'
            }
            receipt=f"codewithwasef_{int(time())}"
            order=client.order.create({'receipt':receipt,"notes":notes,"amount":amount,"currency":currency})
            payment=Payment()
            payment.user=user
            payment.course=course
            payment.order_id=order.get('id')
            payment.save()

    context={
        'course':course,
        'order':order,
        'payment':payment,
        'user':user,
        'error':error,
    }

    return render(request,template_name='courses/checkout.html',context=context)

@csrf_exempt
def verifypayment(request):
    if request.method=='POST':
        data=request.POST
        context={}
        print(data)
        try:
            client.utility.verify_payment_signature(data)
            # change payment adress

            razorpay_payment_id=data['razorpay_payment_id']
            razorpay_order_id=data['razorpay_order_id']
            payment=Payment.objects.get(order_id=razorpay_order_id)
            payment.payment_id=razorpay_payment_id
            payment.status=True
            usercourse=UserCourse(user=payment.user,course=payment.course)
            # usercourse=usercourse.save()
            usercourse.save()
            print(usercourse)
            payment.user_course=usercourse
            payment.save()
            print(usercourse)
            return redirect('my-courses')
            # return render(request,template_name='courses/my_courses.html',context=context)
        except Exception as e :
            return HttpResponse("Invalid payment : %s" % str(e))
        
