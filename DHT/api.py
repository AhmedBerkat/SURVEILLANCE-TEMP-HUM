from .models import Dht11
from .serializers import DHT11serialize
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
import requests

# Définir la fonction pour envoyer des messages Telegram
def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")
    return response

@api_view(["GET", "POST"])
def Dlist(request):
    if request.method == "GET":
        all_data = Dht11.objects.all()
        data_ser = DHT11serialize(all_data, many=True)  # Les données sont sérialisées en JSON
        return Response(data_ser.data)

    elif request.method == "POST":
        serial = DHT11serialize(data=request.data)

        if serial.is_valid():
            serial.save()
            derniere_temperature = Dht11.objects.last().temp
            print(f"Latest temperature: {derniere_temperature}")

            if derniere_temperature > 25:
                # Alert Email
                subject = 'Alerte'
                message = 'La température dépasse le seuil de 25°C, veuillez intervenir immédiatement pour vérifier et corriger cette situation'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['ahmedberkat664@gmail.com']
                send_mail(subject, message, email_from, recipient_list)
                print("Email sent successfully.")

                # Alert Telegram
                telegram_token = settings.TELEGRAM_TOKEN
                chat_id = settings.TELEGRAM_CHAT_ID
                telegram_message = 'La température dépasse le seuil de 25°C, veuillez intervenir immédiatement pour vérifier et corriger cette situation'
                response = send_telegram_message(telegram_token, chat_id, telegram_message)
                if response.status_code == 200:
                    print("Telegram message sent successfully.")
                else:
                    print(f"Failed to send Telegram message: {response.text}")

            return Response(serial.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
