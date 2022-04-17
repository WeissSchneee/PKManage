from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
class Position(models.Model):
    positionid = models.CharField(max_length=10,primary_key=True)
    status = models.BooleanField(default=True)
    zoon = models.CharField(max_length=4)
    name = models.IntegerField()
    distance = models.IntegerField()

class Car(models.Model):
    License = models.CharField(max_length=7,primary_key=True)
    Time = models.DateTimeField()
    Counter = models.IntegerField(validators=[MinValueValidator(0)])
    Position = models.ForeignKey(to='Position',on_delete=models.CASCADE,default='')
    Charge = models.IntegerField()


