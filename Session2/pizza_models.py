from operator import truediv
from django.db import models


class MainTopping(models.Model):
    name = models.CharField(max_length=20)

class SubTopping(models.Model):
    name = models.CharField(max_length=20)
# class Cheese(models.Model):
#     type = models.CharField(max_length=20)
# class Paseley(models.Model):
#     type = models.BooleanField(default = True)
# class Sauce(models.Model):
    # type = models.CharField(max_length=20)

class OnionMushroom(models.Model):
    # type = models.BooleanField(default = True)
    name = models.CharField(max_length=10)
    # 재료 입장에서는 여러 가지 피자에 들어갈 수 있음
    # 피자 입장에서는 버섯 또는 양파 하나씩만 들어감.
    # ForeignKey




class Drink(models.Model):
    name = models.CharField(max_length=20)

class Pizza(models.Model):
    name = models.CharField(max_length=50)
    main_topping = models.OneToOneField(MainTopping, on_delete = models.CASCADE, related_name=name, primary_key=True)
    sub_topping = models.ManyToManyField(SubTopping)
    onion_mushroom = models.ForeignKey(OnionMushroom, on_delete = models.CASCADE, related_name=name)
    # dough = models.CharField(max_length=20)
    # sauce = models.CharField(max_length=20)

    drink = models.ForeignKey("Drink", on_delete=models.CASCADE)
    
