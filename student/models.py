from django.db import models
from django.contrib.auth.models import User
import json
# Create your models here.
class Login_time(models.Model):
    user_id=models.OneToOneField(User, on_delete=models.CASCADE)
    last_login=models.CharField(max_length=20, null=True)
class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name

class Questions(models.Model):
    questions = models.CharField(max_length=550)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    mark_type = models.IntegerField()
    question_status = models.BooleanField(default=True)
    time_limit = models.TimeField(blank=True, null=True)
    choices = models.CharField(max_length=250, help_text="Enter the choice text",null=True)

    def __str__(self):
        return self.questions
   

class Question_paper(models.Model):
    question_id = models.ManyToManyField(Questions)
    question_code=models.CharField( max_length=50)

class submission(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    question_id=models.ForeignKey(Question_paper, on_delete=models.CASCADE)
    submission_time = models.DateTimeField(auto_now_add=True)
    exam_start_time = models.DateTimeField(null=True, blank=True)
    exam_end_time = models.DateTimeField(null=True, blank=True)
    
    total_mark=models.IntegerField()


class TimeForQuestion(models.Model):
    submission = models.ForeignKey('submission', on_delete=models.CASCADE)
    question = models.ForeignKey('Questions', on_delete=models.CASCADE)
    time_taken = models.DurationField()
    answer_selected=models.CharField( max_length=100)
    correct_or_wrong=models.BooleanField()

