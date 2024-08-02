from django.contrib import admin
from django.contrib import admin
from courses.models import Course,Tag,Prerequisite,Learning,Video,quiz_model
from courses.models import UserCourse,Payment
from django.utils.html import format_html
class TagAdmin(admin.TabularInline):
    model=Tag

class LearningAdmin(admin.TabularInline):
    model=Learning

class PrerequisiteAdmin(admin.TabularInline):
    model=Prerequisite

class QuizAdmin(admin.TabularInline):
    model=quiz_model



class VideoAdmin(admin.TabularInline):
    model=Video

class CourseAdmin(admin.ModelAdmin):
    inlines=[TagAdmin,PrerequisiteAdmin,LearningAdmin,VideoAdmin,QuizAdmin]
    list_display=['name','get_price','get_discount','active']
    list_filter=('discount','active')
    def get_discount(self,course):
        return f'{course.discount}%'
    def get_price(self,course):
        return f'₹{course.price}'
   

class PaymmentAdmin(admin.ModelAdmin):
    model=Payment
    list_display=['payment_id','user_get','course_get','status']
    list_filter=['status','course']
    def user_get(self,payment):
        return format_html(f"<a target='_blank' href='/admin/auth/user/{payment.user.id}'>{payment.user}</a>")

    def course_get(self,payment):
        return format_html(f"<a target='_blank' href='/admin/courses/course/{payment.course.id}'>{payment.course}</a>")


class usercourseAdminModel(admin.ModelAdmin):
    list_display=['user_get','course_get']
    list_filter=['course','user']
    def user_get(self,usercourse):
        return format_html(f"<a target='_blank' href='/admin/auth/user/{usercourse.user.id}'>{usercourse.user}</a>")

    def course_get(self,usercourse):
        return format_html(f"<a target='_blank' href='/admin/courses/course/{usercourse.course.id}'>{usercourse.course}</a>")




admin.site.register(Course,CourseAdmin)
admin.site.register(Video)
admin.site.register(Payment,PaymmentAdmin)
admin.site.register(UserCourse,usercourseAdminModel)

