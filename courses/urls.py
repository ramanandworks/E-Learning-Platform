from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse
from courses.views import home,coursepage,signupview,loginview,signout,checkout,verifypayment,my_courses


from courses.views.courses import quiz_model,quiz_questions,quizpart,home_quiz,profile,enroll_view

from django.conf.urls.static import static
from django.conf import settings

from courses.views.courses import send_certificate_email

from codewithwasef.settings import MEDIA_URL,MEDIA_ROOT

urlpatterns = [
    path('',home,name='home'),
    path('logout',signout,name='logout'),
    path('profile',profile,name='profile'),
    path('my-courses',my_courses,name='my-courses'),
    path('signup',signupview.as_view(),name='signup'),
    path('login',loginview.as_view(),name='login'),
    path('course/<str:slug>',coursepage,name='coursepage'),

    path('checkout/<str:slug>',checkout,name='checkout'),
    path('verify_payment',verifypayment,name='verify_payment'),

    path('course/<str:slug>/home_quiz',home_quiz,name='home_quiz'),
    path('course/<str:slug>/quiz',quiz_questions,name='quiz'),
    path('course/<str:slug>/score',quizpart,name='score'),


path('send-email/', send_certificate_email, name='send_email_with_attachment'),

path('course/<slug:slug>/enroll/', enroll_view, name='enroll'),

]+static(MEDIA_URL,document_root=MEDIA_ROOT)

urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)