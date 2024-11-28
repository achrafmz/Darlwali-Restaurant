# utils.py
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Restaurant
import re
from django.core.mail import BadHeaderError
def send_confirmation_email(reservation):
    try:
        subject = 'Confirmation de Réservation'
        message = "Votre réservation a été confirmée."
        
        send_mail(
            subject,
            message,
            'achrafmazouz50@gmail.com@gmail.com',
            [reservation.email],
            fail_silently=False,
        )
        print("Email envoyé avec succès")
    except BadHeaderError:
        print("Erreur de header invalide.")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")
