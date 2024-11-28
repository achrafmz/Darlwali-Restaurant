from django.shortcuts import render,redirect,get_object_or_404
from .models import Restaurant,Contact,Category,Menu,Reservation,Table,Menu,Category,RestaurantGallery
from django.contrib.auth.decorators import login_required
from .forms import ReservationForm
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.http import HttpResponseRedirect
from .models import Reservation
from .forms import ReservationSearchForm,RestaurantUpdateForm,CategoryForm, MenuForm,RestaurantGalleryForm,ProfileUpdateForm,CustomPasswordChangeForm,TableForm
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
import openai
from django.conf import settings
import requests
import google.generativeai as genai
import os
import random
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
from django.contrib.auth.forms import UserCreationForm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .utils import send_confirmation_email  # Importez votre fonction d'envoi d'e-mail
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from datetime import datetime, timedelta
from django.db.models import Q
from django.contrib.auth import logout
from django.core.mail import EmailMessage



















def home(request):
    restaurant = Restaurant.objects.first()  # Récupérer le premier restaurant
    
    if request.method == 'POST':
        # Récupérer les données du formulaire
        prenom = request.POST.get('prenom')
        nom = request.POST.get('nom')
        email = request.POST.get('mail')
        message = request.POST.get('message')

        # Vérification des champs vides
        if not prenom or not nom or not email or not message:
            context = {
                'restaurant': restaurant,
                'error_message': 'Tous les champs sont obligatoires.'
            }
            return render(request, 'home.html', context)
        
        # Enregistrer les données dans la base de données
        contact = Contact(firstname=prenom, lastname=nom, email=email, message=message)
        contact.save()

        # Envoyer un e-mail de confirmation à l'utilisateur
        subject = 'Confirmation de la réception de votre message'
        message_body = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            color: #333;
        }}
        .container {{
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .header img {{
            max-width: 150px;
        }}
        .content {{
            text-align: center;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            font-size: 0.8em;
            color: #666;
        }}
        a {{
            color: #1a73e8;
            text-decoration: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="https://achrafmazouz1.000webhostapp.com/logogo.jpg" alt="Logo de Dar Lwali"> <!-- Remplacez par l'URL de votre logo -->
            <h1>Confirmation de réception de votre message</h1>
        </div>
        <div class="content">
            <p>Bonjour {prenom} {nom},</p>
            <p>Nous avons bien reçu votre message et nous vous remercions de nous avoir contactés.</p>
            <p>Voici le contenu de votre message :</p>
            <p><strong>{message}</strong></p>
            <p>Nous vous répondrons dans les plus brefs délais. Si vous avez d'autres questions, n'hésitez pas à nous contacter au <strong>{restaurant.phone}</strong> ou par e-mail à <strong>darlwali@gmail.com</strong>.</p>
            <p>Merci pour votre patience et à bientôt !</p>
        </div>
        <div class="footer">
            <p>{restaurant.address}</p>
            <p>Téléphone : {restaurant.phone}</p>
        </div>
    </div>
</body>
</html>
        """
        from_email = 'votre-email@gmail.com'  # Remplacez par votre adresse e-mail
        recipient_list = [email]

        email = EmailMessage(subject, message_body, from_email, recipient_list)
        email.content_subtype = 'html'  # Spécifie que le contenu est en HTML
        email.send()

        # Afficher un message de succès
        context = {
            'restaurant': restaurant,
            'message': 'Message envoyé avec succès!'
        }
        return render(request, 'home.html', context)
    
    # Contexte par défaut si aucune donnée n'est soumise
    context = {
        'restaurant': restaurant
    }
    return render(request, 'home.html', context)

def menu(request):
    restaurant = Restaurant.objects.first()  # Récupérer le premier restaurant
    categories = Category.objects.all()  # Récupérer toutes les catégories
    menus = Menu.objects.all()  # Récupérer tous les éléments du menu
    
    context = {
        'restaurant': restaurant,
        'categories': categories,
        'menus': menus,
    }
    return render(request, 'menu.html', context)


def reservation_success_view(request):
    # Récupère le premier restaurant dans la base de données
    restaurant = Restaurant.objects.first()
    
    # Récupère l'ID de la réservation à partir des paramètres GET
    reservation_id = request.GET.get('reservation_id')
    
    # Récupère l'objet Reservation correspondant à l'ID
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    # Passe les informations de la réservation et du restaurant au template
    return render(request, 'reservation_success.html', {
        'reservation': reservation,
        'restaurant': restaurant
    })


def reservation(request):
    restaurant = Restaurant.objects.first()
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            number_of_people = form.cleaned_data['number_of_people']
            email = form.cleaned_data['email']

            # Combiner date et heure en un datetime complet et rendre le datetime conscient du fuseau horaire
            reservation_datetime = timezone.make_aware(datetime.combine(date, time), timezone.get_current_timezone())

            # Vérifier si la date ou l'heure est dans le passé
            if reservation_datetime < timezone.now():
                messages.error(request, "La date ou l'heure choisie est déjà passée. Veuillez choisir une autre date ou heure.")
            else:
                # Créer la période de réservation
                end_time = (datetime.combine(date, time) + timedelta(hours=2)).time()
                end_datetime = timezone.make_aware(datetime.combine(date, end_time), timezone.get_current_timezone())

                # Trouver les tables disponibles
                available_tables = Table.objects.filter(
                    seats__gte=number_of_people
                ).exclude(
                    Q(reservation__date=date) &
                    Q(reservation__time__gte=time) &
                    Q(reservation__time__lt=end_time)
                ).distinct()

                if available_tables.exists():
                    reservation = form.save(commit=False)
                    
                    # Vérifier si l'utilisateur est authentifié
                    if request.user.is_authenticated:
                        reservation.user = request.user
                    else:
                        reservation.user = None
                    
                    reservation.table = available_tables.first()
                    reservation.save()

                    # Envoyer un e-mail de confirmation
                    subject = 'Confirmation de votre réservation'
                    message = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            color: #333;
        }}
        .container {{
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .header img {{
            max-width: 150px;
        }}
        .content {{
            text-align: center;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            font-size: 0.8em;
            color: #666;
        }}
        a {{
            color: #1a73e8;
            text-decoration: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="https://achrafmazouz1.000webhostapp.com/logogo.jpg" alt="Logo de Dar Lwali"> <!-- Remplacez par l'URL de votre logo -->
            <h1>Confirmation de votre réservation</h1>
        </div>
        <div class="content">
            <p>Bonjour {first_name} {last_name},</p>
            <p>Nous avons le plaisir de vous confirmer votre réservation au <strong>Dar Lwali</strong>.</p>
            <p>Voici les détails de votre réservation :</p>
            <ul>
                <li><strong>Date</strong> : {date}</li>
                <li><strong>Heure</strong> : {time}</li>
                <li><strong>Nombre de personnes</strong> : {number_of_people}</li>
            </ul>
            <p>Nous avons réservé une table pour vous à la date et l'heure choisies. Nous vous attendons avec impatience et nous ferons de notre mieux pour rendre votre expérience agréable.</p>
            <p>Si vous avez des questions ou si vous devez apporter des modifications à votre réservation, n'hésitez pas à nous contacter au <strong>{restaurant.phone}</strong> ou par e-mail à <strong>darlwali@gmail.com</strong>.</p>
            <p>Merci de votre confiance et à bientôt au <strong>Dar Lwali</strong> !</p>
        </div>
        <div class="footer">
            <p>{restaurant.address}</p>
            <p>Téléphone : {restaurant.phone}</p>
        </div>
    </div>
</body>
</html>
                    """
                    from_email = 'votre-email@gmail.com'  # Remplacez par votre adresse e-mail
                    recipient_list = [email]

                    email = EmailMessage(subject, message, from_email, recipient_list)
                    email.content_subtype = 'html'  # Spécifie que le contenu est en HTML
                    email.send()

                    return redirect(reverse('reservation_success') + f'?reservation_id={reservation.id}')
                else:
                    messages.error(request, "Désolé, aucune table disponible pour cette date et heure.")
    else:
        form = ReservationForm()

    return render(request, 'reservation.html', {
        'form': form,
        'restaurant': restaurant
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Récupère les données de réservation stockées dans la session
            reservation_form_data = request.session.pop('reservation_form_data', None)
            if reservation_form_data:
                request.POST = reservation_form_data  # Réinitialise la demande POST avec les données de réservation
                return redirect('reservation')  # Redirection vers la vue de réservation
            return redirect('home')  # Remplacez par l'URL de la page d'accueil ou autre
    else:
        form = AuthenticationForm()

    return render(request, 'loginadmin.html', {'form': form})

@login_required(login_url='/adminlogin/')
def dashboard(request):
    # Récupérer les messages de contact
    messages = Contact.objects.all().order_by('-date_posted')
    
    # Exemple de données fictives pour le tableau de bord
    context = {
        'message_count': Contact.objects.count(),
        'reservation_count': Reservation.objects.count(),
        'messages': messages,  # Ajouter les messages au contexte
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='/adminlogin/')
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/reservation-list/'))

@login_required(login_url='/adminlogin/')
def reservation_list(request):
    form = ReservationSearchForm(request.GET or None)
    reservations = Reservation.objects.all()

    if form.is_valid():
        reservation_id = form.cleaned_data.get('reservation_id')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')

        if reservation_id:
            reservations = reservations.filter(id=reservation_id)
        if date_from:
            reservations = reservations.filter(date__gte=date_from)
        if date_to:
            # Ajout d'un jour à la date de fin pour inclure toute la journée
            date_to = date_to + timezone.timedelta(days=1)
            reservations = reservations.filter(date__lte=date_to)

    context = {
        'form': form,
        'reservations': reservations,
    }
    return render(request, 'reservation_list.html', context)

@login_required(login_url='/adminlogin/')
def update_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reservation_list')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'update_reservation.html', {'form': form})

@login_required(login_url='/adminlogin/')
def update_restaurant(request):
    restaurant = Restaurant.objects.first()  # Récupère le premier restaurant dans la base de données

    if not restaurant:
        return redirect('some_error_page')  # Redirigez vers une page d'erreur si aucun restaurant n'est trouvé

    if request.method == 'POST':
        form = RestaurantUpdateForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirigez vers le tableau de bord ou une autre page
    else:
        form = RestaurantUpdateForm(instance=restaurant)

    context = {
        'form': form,
        'restaurant': restaurant
    }
    return render(request, 'update_restaurant.html', context)

@login_required(login_url='/adminlogin/')
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

@login_required(login_url='/adminlogin/')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})

@login_required(login_url='/adminlogin/')
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'edit_category.html', {'form': form})

@login_required(login_url='/adminlogin/')
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'delete_category.html', {'category': category})
@login_required(login_url='/adminlogin/')
def menu_list(request):
    # Récupérer toutes les catégories
    categories = Category.objects.all()

    # Récupérer la catégorie sélectionnée dans le formulaire
    category_id = request.GET.get('category')

    # Filtrer les éléments du menu par catégorie, ou récupérer tous les éléments si aucune catégorie n'est sélectionnée
    if category_id:
        menu_items = Menu.objects.filter(category_id=category_id)
    else:
        menu_items = Menu.objects.all()

    context = {
        'categories': categories,
        'menu_items': menu_items,
    }
    return render(request, 'menu_list.html', context)

@login_required(login_url='/adminlogin/')
def add_menu_item(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuForm()
    return render(request, 'add_menu_item.html', {'form': form})

@login_required(login_url='/adminlogin/')

def edit_menu_item(request, pk):
    item = get_object_or_404(Menu, pk=pk)
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuForm(instance=item)
    return render(request, 'edit_menu_item.html', {'form': form, 'item': item})

@login_required(login_url='/adminlogin/')
def delete_menu_item(request, pk):
    menu_item = get_object_or_404(Menu, pk=pk)
    if request.method == 'POST':
        menu_item.delete()
        return redirect('menu_list')
    return render(request, 'delete_menu_item.html', {'menu_item': menu_item})

@login_required(login_url='/adminlogin/')

def gallery_list(request):
    gallery_images = RestaurantGallery.objects.all()
    return render(request, 'gallery_list.html', {'gallery_images': gallery_images})
@login_required(login_url='/adminlogin/')
def add_gallery_image(request):
    if request.method == 'POST':
        form = RestaurantGalleryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery_list')
    else:
        form = RestaurantGalleryForm()
    return render(request, 'add_gallery_image.html', {'form': form})

@login_required(login_url='/adminlogin/')
def edit_gallery_image(request, pk):
    image = get_object_or_404(RestaurantGallery, pk=pk)
    if request.method == 'POST':
        form = RestaurantGalleryForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            return redirect('gallery_list')
    else:
        form = RestaurantGalleryForm(instance=image)
    return render(request, 'edit_gallery_image.html', {'form': form, 'image': image})

@login_required(login_url='/adminlogin/')

def delete_gallery_image(request, pk):
    image = get_object_or_404(RestaurantGallery, pk=pk)
    if request.method == 'POST':
        image.delete()
        return redirect('gallery_list')
    return render(request, 'delete_gallery_image.html', {'image': image})


@login_required(login_url='/adminlogin/')

def delete_message(request, id):
    message = get_object_or_404(Contact, id=id)
    message.delete()
    return redirect('contact_list')
@login_required(login_url='/adminlogin/')

def contact_list(request):
    messages = Contact.objects.all().order_by('-date_posted')  
    return render(request, 'contact_list.html', {'messages': messages})

@login_required(login_url='/adminlogin/')
def view_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'view_reservation.html', {'reservation': reservation})

def adminlogin(request):
    # Si l'utilisateur est déjà connecté, redirigez-le vers le tableau de bord admin
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard')  # Redirige vers le tableau de bord si déjà connecté

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Vérification du statut admin (is_staff) et de l'activation du compte (is_active)
            if user.is_staff and user.is_active:
                login(request, user)
                return redirect('dashboard')  # Redirection vers le tableau de bord admin
            else:
                messages.error(request, "Vous n'avez pas les droits nécessaires pour accéder à cette page.")
        else:
            messages.error(request, "Identifiants invalides. Veuillez réessayer.")
    
    else:
        form = AuthenticationForm()
    
    return render(request, 'loginadmin.html', {'form': form})


def admin_logout(request):
    logout(request)
    print("Utilisateur déconnecté")
    return redirect('adminlogin')

@login_required(login_url='/adminlogin/')
def profile_view(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        if profile_form.is_valid() and password_form.is_valid():
            profile_form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)  # Keeps the user logged in after password change
            return redirect('profile')
    else:
        profile_form = ProfileUpdateForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'profile.html', {
        'profile_form': profile_form,
        'password_form': password_form
    })




def chatbot(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip().lower()

        # Définir des menus comme des listes de plats
        menus = {
            "entrée": ["Salade marocaine", "Harira", "Briouates"],
            "plat principal": ["Couscous Royal", "Tajine de poulet", "Pastilla"],
            "dessert": ["Chebakia", "Makroud", "Tarte aux pommes"],
            "boisson": ["Thé à la menthe", "Jus d'orange frais", "Soda"]
        }

        # Messages de bienvenue
        welcome_messages = [
            "Bonjour ! Comment puis-je vous aider aujourd'hui ?",
            "Salut ! Bienvenue chez DAR LWALI. Comment puis-je vous assister ?",
            "Hello ! En quoi puis-je vous être utile ?",
            "Bienvenue ! Que puis-je faire pour vous ?"
        ]

        # Logique de réponse améliorée
        if 'hey' in user_message or 'hello' in user_message or 'salut' in user_message:
            response = random.choice(welcome_messages)
        elif 'horaire' in user_message:
            response = "Nous sommes ouverts tous les jours de 9h à 22h. Besoin d'une réservation pour un créneau spécifique ?"
        elif 'menu' in user_message:
            # Recommander un plat aléatoire de la catégorie 'plat principal'
            response = f"Notre menu inclut des plats délicieux comme {random.choice(menus['plat principal'])}. Vous pouvez consulter le menu complet sur notre page dédiée."
        elif 'réserver' in user_message or 'reservation' in user_message:
            response = "Pour effectuer une réservation, vous pouvez utiliser notre formulaire en ligne ou nous appeler directement au 01 23 45 67 89."
        elif 'localisation' in user_message or 'où se trouve' in user_message:
            response = "Nous sommes situés au rue ibn tachefine Marrakech. Vous pouvez nous trouver facilement avec Google Maps !"
        elif 'que sommes-nous' in user_message:
            response = "Nous sommes un restaurant passionné par la cuisine marocaine traditionnelle et les produits frais. Venez découvrir nos spécialités préparées avec soin !"
        elif 'recommande' in user_message or 'plat' in user_message:
            # Recommander un plat aléatoire en fonction de la catégorie demandée
            if 'entrée' in user_message:
                category = 'entrée'
            elif 'plat' in user_message:
                category = 'plat principal'
            elif 'dessert' in user_message:
                category = 'dessert'
            elif 'boisson' in user_message:
                category = 'boisson'
            else:
                category = random.choice(list(menus.keys()))
                
            response = f"Je vous recommande notre {random.choice(menus[category])} de la catégorie {category}. C'est un plat très apprécié par nos clients !"
        else:
            # Réponse dynamique en cas d'incertitude
            apologies = [
                "Désolé, je ne comprends pas encore cette question.",
                "Je ne suis pas sûr de comprendre. Pouvez-vous reformuler ?",
                "Hmm, cette question est un peu difficile pour moi. Essayez autre chose !"
            ]
            response = random.choice(apologies)

        return JsonResponse({'response': response})

    return render(request, 'chat.html')

@login_required(login_url='/adminlogin/')
def edit_table(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    if request.method == 'POST':
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            return redirect('table_list')  # Rediriger vers une vue listant les tables par exemple
    else:
        form = TableForm(instance=table)
    return render(request, 'edit_table.html', {'form': form})

@login_required(login_url='/adminlogin/')

def add_table(request):
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('table_list')  # Rediriger vers une vue listant les tables par exemple
    else:
        form = TableForm()
    return render(request, 'add_table.html', {'form': form})

@login_required(login_url='/adminlogin/')

def send_reply(request, message_id):
    contact = get_object_or_404(Contact, id=message_id)

    if request.method == 'POST':
        response_message = request.POST.get('response')
        if response_message:
            # Envoyer l'e-mail
            subject = 'Réponse à votre message'
            message = f"""
Bonjour {contact.firstname} {contact.lastname},

Merci pour votre message. Voici notre réponse :

{response_message}

Nous restons à votre disposition pour toute autre question.

Cordialement,
L'équipe de Dar Lwali
            """
            from_email = 'votre-email@gmail.com'
            recipient_list = [contact.email]
            
            send_mail(subject, message, from_email, recipient_list)
            
            messages.success(request, 'Réponse envoyée avec succès !')
            return redirect('contact_list')
        else:
            messages.error(request, 'Le message de réponse ne peut pas être vide.')

    return redirect('contact_list')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Rediriger vers la page de connexion après l'inscription
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def download_reservation(request, reservation_id):
    # Récupère l'objet Reservation et Restaurant
    reservation = get_object_or_404(Reservation, id=reservation_id)
    restaurant = Restaurant.objects.first()
    
    # Crée un objet HttpResponse avec le type de contenu approprié pour un fichier PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reservation_{reservation_id}.pdf"'
    
    # Crée un objet Canvas pour générer le PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Ajouter le logo du restaurant
    try:
        logo_path = 'https://achrafmazouz1.000webhostapp.com/logogo.jpg'  # Chemin vers l'image du logo
        p.drawImage(logo_path, x=50, y=height - 100, width=100, height=50)
    except:
        p.drawString(50, height - 100, "Logo du Restaurant")
    
    # Ajouter le nom du restaurant
    p.setFont("Helvetica-Bold", 24)
    p.drawString(200, height - 80, restaurant.name)
    
    # Ajouter une ligne horizontale
    p.setStrokeColor(colors.black)
    p.setLineWidth(1)
    p.line(50, height - 100, width - 50, height - 100)
    
    # Ajouter la date de téléchargement
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 130, f"Date de téléchargement : {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Ajouter les détails de la réservation avec des styles
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 180, "Détails de la Réservation")
    
    p.setFont("Helvetica", 12)
    details = [
        f"ID de réservation : {reservation.id}",
        f"Prénom : {reservation.first_name}",
        f"Nom : {reservation.last_name}",
        f"Téléphone : {reservation.phone}",
        f"Email : {reservation.email}",
        f"Date : {reservation.date.strftime('%d/%m/%Y')}",
        f"Heure : {reservation.time.strftime('%H:%M')}",
        f"Nombre de personnes : {reservation.number_of_people}",
        f"Table : {reservation.table}"
    ]
    
    y_position = height - 210
    for detail in details:
        p.drawString(50, y_position, detail)
        y_position -= 20
    
    # Finaliser le PDF
    p.showPage()
    p.save()
    
    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()
    
    return response

def test_email_view(request):
    try:
        subject = 'Test de Confirmation de Réservation'
        message = 'Ceci est un e-mail de test pour vérifier l\'envoi d\'e-mails.'
        from_email = 'achrafmazouz50@gmail.com@gmail.com'
        recipient_list = ['achrafmazouz50@gmail.com']  # Remplacez par votre adresse e-mail de test
        
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return HttpResponse('Email envoyé avec succès')
    except BadHeaderError:
        return HttpResponse('Erreur de header invalide.')
    except Exception as e:
        return HttpResponse(f'Erreur lors de l\'envoi de l\'email : {e}')