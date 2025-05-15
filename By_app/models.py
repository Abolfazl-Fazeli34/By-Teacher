from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)  # آیا تایید ایمیل انجام شده

    def __str__(self):
        return self.email

from django.db import models
from django.utils import timezone
from datetime import timedelta

class EmailVerificationCode(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f'{self.user.email} - {self.code}'


class Teacher(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='teachers')
    name = models.CharField(max_length=100)
    vote = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TeacherVote(models.Model):
    voter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='teacher_votes')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='votes')
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter', 'teacher')  # یک رأی برای هر معلم توسط هر کاربر



