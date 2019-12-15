from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=255)
    url = models.TextField()
    date = models.DateField()
    votes_total = models.IntegerField(default=1)
    icon = models.ImageField(upload_to='images/')
    image = models.ImageField(upload_to='images/')
    body = models.TextField()
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)

    def summary(self):
        return self.body[:145]

    def __str__(self):
        return self.title


class Vote(models.Model):
    productID = models.ForeignKey(Product,on_delete=models.CASCADE)
    userID = models.ForeignKey(User,on_delete=models.CASCADE)