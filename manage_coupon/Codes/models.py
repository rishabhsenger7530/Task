from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class User(AbstractUser):
    contact = models.CharField(max_length=250, null =False, blank=False)
    email = models.EmailField(max_length=250)
    referralCode =  models.CharField(max_length=32, blank=False, null=False)
    promocodestatus = models.CharField(max_length=32, blank=False, null=False)# 1 for can apply and 0 for not for promocode
    askQuestion = models.PositiveIntegerField(default=10)# 
    


class Productcategory(models.Model):
    name = models.CharField(max_length=250, null =False, blank=False)
    description = models.TextField()
    createdDate = models.DateTimeField(default=datetime.now, blank=True)
    updatedDate = models.DateTimeField(blank=True,null=True)


class Product(models.Model):
    categoryId = models.ForeignKey(Productcategory,on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null =False, blank=False)
    price =  models.FloatField()
    description = models.TextField()
    createdDate = models.DateTimeField(default=datetime.now, blank=True)
    updatedDate = models.DateTimeField(blank=True,null=True)

class ProductInventory(models.Model):
    productId = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    createdDate = models.DateTimeField(default=datetime.now, blank=True)
    updatedDate = models.DateTimeField(blank=True,null=True)

class CodeType(models.Model):
    codeType = models.CharField(max_length=250, unique=True, blank=True)


class Plan(models.Model):
    plan_name = models.CharField(max_length=250, unique=True, blank=True)
    price =  models.FloatField()
    

class Code(models.Model):
    codetypeid = models.ForeignKey(CodeType,on_delete=models.CASCADE)
    code = models.CharField(max_length=32, unique=True, blank=True)
    plan = models.CharField(max_length=50, blank=True, null=True)
    discount = models.PositiveIntegerField(blank=True, null=True)
    amount = models.PositiveBigIntegerField(blank=True, null=True)
    status     = models.BooleanField(default=False)
 

class Codeapply(models.Model):
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    planid = models.ForeignKey(Plan,blank=True, null=True,on_delete=models.SET_NULL)
    codeid = models.ForeignKey(Code,on_delete=models.CASCADE)
    applydate = models.DateTimeField(default=datetime.now, blank=True)


