from django.db import models

# Create your models here.
class contact(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.email
    
class User(models.Model):
    email = models.EmailField()
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    address = models.TextField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email + ' ' + self.fname
    