from django.db import models

# Create your models here.
class contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    mobile=models.CharField(max_length=20)
    msg=models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class sign_up(models.Model):
    name=models.CharField(max_length=120)
    mobile=models.CharField(max_length=20)
    email=models.EmailField(max_length=80, primary_key=True)
    passwd=models.CharField(max_length=80)
    dob=models.DateField()
    ppic=models.ImageField(upload_to='static/profile',default="")
    address=models.TextField(max_length=3000)

    def __str__(self):
        return self.name

class category(models.Model):
    cname=models.CharField(max_length=120)
    cpic=models.ImageField(upload_to='static/category',default="")
    cdate=models.DateField()

    def __self__(self):
        return self.cname


class product(models.Model):
    name=models.CharField(max_length=150)
    ppic=models.ImageField(upload_to='static/products',default="")
    color=models.CharField(max_length=12)
    tprice=models.FloatField()
    disprice=models.FloatField()
    pdes=models.TextField(max_length=5000)
    pdate=models.DateField()
    pcategory=models.ForeignKey(category, on_delete=models.CASCADE)


class order(models.Model):
    pid=models.IntegerField()
    userid=models.EmailField(max_length=100)
    remarks=models.CharField(max_length=40)
    status=models.BooleanField()
    odate=models.DateField()

class addtocart(models.Model):
    pid=models.IntegerField()
    userid=models.EmailField(max_length=100)
    status=models.BooleanField()
    cdate=models.DateField()