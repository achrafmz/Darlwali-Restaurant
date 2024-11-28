from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime



class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    opening_hours = models.CharField(max_length=255)
    closing_hours = models.CharField(max_length=255)
    localisation = models.URLField(blank=True)
    aboutus = models.TextField(blank=True)
    bgphoto = models.ImageField(upload_to='bgphoto/', blank=True, null=True)
    logo = models.ImageField(upload_to='logo/', blank=True, null=True)


    

    def __str__(self):
        return self.name

class RestaurantGallery(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='restaurant_gallery/', blank=True, null=True)
    description = models.CharField(max_length=255, blank=True)  # Vérifiez ce champ

    def __str__(self):
        return f"Image for {self.restaurant.name}"

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Menu(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='menu_photos/', blank=True, null=True)

    def __str__(self):
        return self.name



class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    

    def __str__(self):
        return self.name

class Contact(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.lastname


class Table(models.Model):
    number = models.CharField(max_length=10)
    seats = models.IntegerField()

    def __str__(self):
        return f"Table {self.number} - {self.seats} places"

class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default="00:00")
    number_of_people = models.IntegerField(default=1)

    def __str__(self):
        return f"Reservation for {self.table} on {self.date}"
    
    class Meta:
        unique_together = ['table', 'date', 'time']
class Action(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.description