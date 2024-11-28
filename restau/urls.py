from django.urls import path, include
from . import views 
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('reservation/', views.reservation, name='reservation'),
    path('reservation_success/', views.reservation_success_view, name='reservation_success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('reservation-list/', views.reservation_list, name='reservation_list'),
    path('cancel-reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('update-reservation/<int:reservation_id>/', views.update_reservation, name='update_reservation'),
    path('update-restaurant/', views.update_restaurant, name='update_restaurant'),
     path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),

    path('menus/', views.menu_list, name='menu_list'),
    path('menu/add/', views.add_menu_item, name='add_menu_item'),
    path('menu/edit/<int:pk>/', views.edit_menu_item, name='edit_menu_item'),
    path('menu/delete/<int:pk>/', views.delete_menu_item, name='delete_menu_item'),
    path('gallery/', views.gallery_list, name='gallery_list'),
    path('gallery/add/', views.add_gallery_image, name='add_gallery_image'),
    path('gallery/edit/<int:pk>/', views.edit_gallery_image, name='edit_gallery_image'),
    path('gallery/delete/<int:pk>/', views.delete_gallery_image, name='delete_gallery_image'),
    path('messages/delete/<int:id>/', views.delete_message, name='delete_message'),
    path('contact_list/', views.contact_list, name='contact_list'),
    path('reservation/<int:pk>/', views.view_reservation, name='view_reservation'),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.admin_logout, name='logout'),
    path('chat/', views.chatbot, name='chatbot'),
    path('table/edit/<int:table_id>/', views.edit_table, name='edit_table'),
    path('table/add/', views.add_table, name='add_table'),
    path('download_reservation/<int:reservation_id>/', views.download_reservation, name='download_reservation'),
        path('test-email/', views.test_email_view, name='test_email'),
            path('send-reply/<int:message_id>/', views.send_reply, name='send_reply'),



    





]