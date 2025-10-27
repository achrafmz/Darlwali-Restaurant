from django.contrib import admin
from .models import Restaurant, RestaurantGallery, Menu, Reservation, Contact, Table, Category

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'email', 'opening_hours', 'closing_hours', 'localisation','bgphoto','logo')
    search_fields = ('name', 'address', 'phone')

@admin.register(RestaurantGallery)
class RestaurantGalleryAdmin(admin.ModelAdmin):
    list_display = ('image', 'description')
    search_fields = ('description',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'category', 'photo')
    search_fields = ('name', 'category')
    list_filter = ('category',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'email', 'message','date_posted')
    search_fields = ('lastname', 'email')

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'seats')
    search_fields = ('number',)
    list_filter = ('seats',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('table', 'date', 'time', 'number_of_people')
    search_fields = ('first_name', 'last_name', 'phone', 'email')
    list_filter = ('date', 'time', 'table')
    ordering = ('-date', '-time')
    readonly_fields = ('table', 'date', 'time', 'number_of_people')
