from django.db import models

# Create your models here.
class client(models.Model):
    name = models.CharField(max_length=50)
    mobile = models.IntegerField()
    email = models.EmailField(max_length=254)
    gender = models.CharField(max_length=50)
    
class Questions(models.Model):
    client=models.ForeignKey(client, verbose_name=_(""), on_delete=models.CASCADE)
    questions = models.CharField(max_length=50)
    option_text = models.CharField(max_length=50)
    weight = models.IntegerField()
    
class quesA(models.Model):
    que = models.CharField( max_length=500)
    option1= models.CharField( max_length=1000)
    option2= models.CharField( max_length=1000)
    option3= models.CharField( max_length=1000)
    option4= models.CharField( max_length=1000)