from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save
from django.core.validators import RegexValidator
from django.utils import timezone

phone_regex = RegexValidator(
        regex=r'/^\+?[0-9]{11,11}$/',
        message="Wrong phone number format",
    )


class UserProfile(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20, default='+',)
    birth_date = models.DateField()
    address = models.CharField(max_length=200)
    GENDER_CHOICES = (
     ('M', 'Male'),
     ('F', 'Female'),
    )
    gender = models.CharField(blank=True, max_length=1,
                              choices=GENDER_CHOICES, default='M',)

    objects = UserManager()


def create_custom_user(sender, instance, created, **kwargs):
    if created:
        values = {}
        for field in sender._meta.local_fields:
            values[field.attname] = getattr(instance, field.attname)
        user = UserProfile(**values)
        user.save()

post_save.connect(create_custom_user, User)


class Computer(models.Model):
    PersonalComputer = 'Personal Computer'
    Monoblock = 'Monoblock'
    Laptop = 'Laptop'
    computer_types = {
        (PersonalComputer, 'Personal computer'),
        (Monoblock, 'Monoblock'),
        (Laptop, 'Laptop'),
    }
    name = models.CharField(max_length=255, unique=True, primary_key=True)
    price = models.IntegerField(null=True, default=0)
    description = models.TextField(
        max_length=500, default='No description yet')
    type = models.CharField(
        max_length=30, choices=computer_types, default=PersonalComputer)
    pic = models.ImageField(upload_to='/Users/hp/PycharmProjects/hw/hw/media', blank=True, max_length=1000)
    quantity = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.name


class Order(models.Model):

    date = models.DateTimeField(default=timezone.now)
    items = models.ManyToManyField(Computer, through='BelongTo')
    code = models.AutoField(max_length=6, unique=True, primary_key=True)
    customer = models.ForeignKey(UserProfile)
    total = models.DecimalField(
        decimal_places=2, max_digits=10, unique=False, default=0.0)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return str(self.code)


class BelongTO(models.Model):
    item = models.ForeignKey(Computer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    id = models.CharField(unique=True, primary_key=True, max_length=255)

    def __str__(self):
        return self.id
