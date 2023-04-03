from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from datetime import datetime, timedelta
# Create your models here.


class Profile(models.Model):
    id = models.AutoField
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.JSONField(default=dict, blank=True)
    def __str__(self):
        return self.user.username
    
    
class Designation(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    parent = models.ForeignKey('self', blank=True, default=" ", null=True, on_delete=models.CASCADE)
    designation_holder = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='designation_holder')
    def __str__(self):
        return self.name


class Complain(models.Model):
    id = models.AutoField
    heading = models.CharField(max_length=300)
    description = models.TextField()
    registered_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    registered_to = models.ForeignKey('Designation', on_delete=models.CASCADE)
    registered_date = models.DateField(default=now, db_index=True)
    response_date = models.DateField(default=datetime.utcnow() + timedelta(days=1))
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.heading + " to " + self.registered_to.name
