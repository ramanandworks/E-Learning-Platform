

import os
import io
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from courses.models import Course, Video, quiz_model, UserCourse

@login_required(login_url='login')
def my_courses(request):
    # course = get_object_or_404(Course)
    user = request.user
    user_courses = UserCourse.objects.filter(user=user)
    context = {
        'user_courses': user_courses,
        # 'course':course,
    }
    return render(request, 'courses/my_courses.html', context=context)

def coursepage(request, slug):
    course = get_object_or_404(Course, slug=slug)
    serial_number = request.GET.get('lecture', 1)
    videos = course.video_set.all().order_by("serial_number")
    video = get_object_or_404(Video, serial_number=serial_number, course=course)
    if not video.is_preview and not request.user.is_authenticated:
        return redirect("login")
    if not video.is_preview:
        user_course = UserCourse.objects.filter(user=request.user, course=course).first()
        if not user_course:
            return redirect('checkout', slug=course.slug)
    context = {
        "course": course,
        "video": video,
        'videos': videos,
        'slug': slug,
    }
    return render(request, 'courses/course_page.html', context=context)

def home_quiz(request, slug):
    content = quiz_model.objects.all()
    return render(request, 'courses/home_quiz.html')

def quiz_questions(request, slug):
    course = get_object_or_404(Course, slug=slug)
    questions = course.questions.all()
    context = {
        'course': course,
        'questions': questions,
    }
    return render(request, 'courses/quiz.html', context)

def quizpart(request, slug):
    course = get_object_or_404(Course, slug=slug)
    questions = course.questions.all()
    n = questions.count()

    if request.method == "POST":
        score = sum(1 for question in questions if request.POST.get(f'answer_{question.id}') == question.answer)
        percentage = (score * 100) / n

        if percentage >= 70.0:
            send_certificate_email(request.user.email, score, percentage, n)
            messages.success(request, 'Congratulations! Certificate sent to your email.')
        else:
            messages.error(request, 'Sorry, you did not pass the quiz.')

        context = {
            'score': score,
            'total_question': n,
            'percentage': percentage,
        }
        return render(request, 'courses/score.html', context)

    return render(request, 'courses/quiz.html', {'course': course, 'questions': questions})

def generate_certificate(score, user_name):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    # p.drawString(300, 900, "Course Completion Certificate")
    # p.drawString(300, 800, f"Name: {user_name}")
    # p.drawString(300, 910, f"Score: {score}")
    p.drawString(100, 750, "Course Completion Certificate")
    p.drawString(100, 730, f"Name: {user_name}")
    p.drawString(100, 710, f"Score: {score}")
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

def send_certificate_email(email, score, percentage, n):
    user_name = email.split('@')[0]  # Use part of the email as the user name
    subject = 'Course Completion Certificate'
    context = {
        'score': score,
        'percentage': percentage,
        'n': n,
    }
    html_content = render_to_string('courses/certificate_email.html', context)
    text_content = strip_tags(html_content)
    email_message = EmailMessage(subject, text_content, to=[email])
    certificate_buffer = generate_certificate(score, user_name)
    email_message.attach('certificate.pdf', certificate_buffer.getvalue(), 'application/pdf')
    email_message.send()
    print(f"Certificate sent to {email}")

@login_required(login_url='login')
def profile(request):
    user = request.user
    first_name = user.first_name.upper()
    last_name = user.last_name.upper()
    email = user.email
    user_courses = UserCourse.objects.filter(user=user)
    context = {
        'user_courses': user_courses,
        'first_name': first_name,
        'last_name': last_name,
        'email': email
    }
    return render(request, 'courses/profile.html', context=context)


def enroll_view(request, slug):
    course = get_object_or_404(Course, slug=slug)
    # Logic to enroll the user in the course
    # ...
    return render(request, 'course/enroll.html', {'course': course})