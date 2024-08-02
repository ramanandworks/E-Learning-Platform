from django.db import models

class Course(models.Model):
    name=models.CharField(max_length=100,null=False)
    slug=models.CharField(max_length=50,null=False,unique=True)
    description=models.CharField(max_length=200,null=True)
    price=models.IntegerField(null=False)
    discount=models.IntegerField(null=False,default=0)
    active=models.BooleanField(default=False)
    thumblain=models.ImageField(upload_to="files/thumblain")
    date=models.DateTimeField(auto_now_add=True)
    resource=models.FileField(upload_to="files/resourses")
    length=models.IntegerField(null=False)

    def __str__(self):
        return self.name


class CourseProperty(models.Model):
    discription=models.CharField(max_length=40,null=False)
    course=models.ForeignKey(Course,null=False,on_delete=models.CASCADE)
    class Meta:
        abstract=True


class quiz_model(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,related_name='questions')
    sl_no=models.IntegerField()
    question = models.CharField(max_length=200)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    answer = models.CharField(max_length=200,null=False)



class Tag(CourseProperty):
    pass

class Prerequisite(CourseProperty):
    pass

class Learning(CourseProperty):
    pass