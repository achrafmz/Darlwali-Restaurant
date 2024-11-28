from django import forms
from .models import Reservation,Restaurant,Category,Menu,RestaurantGallery,Table
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm



class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['first_name', 'last_name', 'phone', 'email', 'date', 'time', 'number_of_people']
        widgets = {
            'date': forms.SelectDateWidget(),
            'time': forms.TimeInput(format='%H:%M'),
        }



class ReservationSearchForm(forms.Form):
    reservation_id = forms.IntegerField(required=False, label='Reservation ID')
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='From Date'
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='To Date'
    )

class RestaurantUpdateForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = [
            'name', 'address', 'phone', 'email', 
            'opening_hours', 'closing_hours', 
            'localisation', 'aboutus', 'bgphoto', 'logo'
        ]
        widgets = {
            'opening_hours': forms.TimeInput(format='%H:%M'),
            'closing_hours': forms.TimeInput(format='%H:%M'),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'description', 'price', 'category', 'photo']

class RestaurantGalleryForm(forms.ModelForm):
     class Meta:
        model = RestaurantGallery
        fields = ['restaurant', 'image', 'description']



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class CustomPasswordChangeForm(PasswordChangeForm):
    pass  # No need to override __init__ unless you are customizing form behavior

class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['number', 'seats']