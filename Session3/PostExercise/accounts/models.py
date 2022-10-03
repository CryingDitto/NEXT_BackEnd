from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Major(models.Model):
    type = models.CharField(max_length=20) # 본전공 심화 이중 융합
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# use django's default User model
# connect User model with my Profile model
# - User model has username and password
# - Profile modes does not have important information
# user Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    # password = models.CharField(max_length=30)
    student_id = models.CharField(max_length=30)    
    name = models.CharField(max_length=50)
    major_main = models.ForeignKey(Major, on_delete=models.SET_NULL, related_name="student_main", null = True)
    major_sub = models.ForeignKey(Major, on_delete=models.SET_NULL, related_name="student_sub", null = True)

    def __str__(self):
        return self.name