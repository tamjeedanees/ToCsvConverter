from django.db import models

# Create your models here.

class Files(models.Model):
    file = models.FileField(upload_to="files")

    def __str__(self):
        return self.file.name

class Contact(models.Model):
    name= models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    text= models.TextField()

    def __str__(self):
        return self.email + " " +self.subject