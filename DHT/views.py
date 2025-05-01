from django.shortcuts import render
from .models import Dht11  # Assurez-vous d'importer le modèle Dht11
from django.utils import timezone
import csv
from django.http import HttpResponse
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm

def home(request):
    return render(request, 'home.html')


def register_view(request):
    if request.method == 'POST':

        type_user = request.POST['type_user']

        password = request.POST['password']

        new_user = User(type_user=type_user, password=make_password(password))
        new_user.save()
        return redirect('login_view')

    return render(request, 'register.html')

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == 'POST':
        type_user = request.POST.get('type_user')
        password = request.POST.get('password')

        user = authenticate(request, type_user=type_user, password=password)

        if user is not None:
            login(request, user)
            # Redirection basée sur le type_user uniquement
            if user.type_user == 'admin':
                return redirect('/admin/')  # Admin Django standard
            return redirect('table')  # Visiteurs

        return render(request, 'login.html', {'error': 'Identifiants incorrects'})

    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def table(request):
    derniere_ligne = Dht11.objects.last()

    if derniere_ligne:
        derniere_date = derniere_ligne.dt
        delta_temps = timezone.now() - derniere_date
        difference_minutes = delta_temps.seconds // 60
        temps_ecoule = ' il y a ' + str(difference_minutes) + ' min'
        if difference_minutes > 60:
            temps_ecoule = 'il y a ' + str(difference_minutes // 60) + 'h' + str(difference_minutes % 60) + 'min'

        valeurs = {
            'date': temps_ecoule,
            'id': derniere_ligne.id,
            'temp': derniere_ligne.temp,
            'hum': derniere_ligne.hum
        }
    else:
        # valeurs par défaut si la base est vide
        valeurs = {
            'date': 'Aucune donnée',
            'id': 0,
            'temp': 0,
            'hum': 0
        }

    return render(request, 'value.html', {'valeurs': valeurs})


@login_required
def download_csv(request):
    model_values = Dht11.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dht.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'temp', 'hum', 'dt'])
    liste = model_values.values_list('id', 'temp', 'hum', 'dt')
    for row in liste:
        writer.writerow(row)
    return response
#pour afficher navbar de template


#pour afficher les graphes
@login_required
def graphiqueTemp(request):
    return render(request, 'ChartTemp.html')
# récupérer toutes les valeur de température et humidity sous forme un #fichier json
@login_required
def graphiqueHum(request):
    return render(request, 'ChartHum.html')
# récupérer toutes les valeur de température et humidity sous forme un #fichier json
@login_required
def chart_data(request):
    dht = Dht11.objects.all()

    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)
@login_required
def chart_data(request):
    dht = Dht11.objects.all()

    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)

#pour récupérer les valeurs de température et humidité de dernier 24h
# et envoie sous forme JSON
@login_required
def chart_data_jour(request):
    dht = Dht11.objects.all()
    now = timezone.now()

    # Récupérer l'heure il y a 24 heures
    last_24_hours = now - timezone.timedelta(hours=24)

    # Récupérer tous les objets de Module créés au cours des 24 dernières heures
    dht = Dht11.objects.filter(dt__range=(last_24_hours, now))
    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)

#pour récupérer les valeurs de température et humidité de dernier semaine
# et envoie sous forme JSON
@login_required
def chart_data_semaine(request):
    dht = Dht11.objects.all()
    # calcul de la date de début de la semaine dernière
    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=7)
    print(datetime.timedelta(days=7))
    print(date_debut_semaine)

    # filtrer les enregistrements créés depuis le début de la semaine dernière
    dht = Dht11.objects.filter(dt__gte=date_debut_semaine)

    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }

    return JsonResponse(data)

#pour récupérer les valeurs de température et humidité de dernier moins
# et envoie sous forme JSON
@login_required
def chart_data_mois(request):
    dht = Dht11.objects.all()

    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=30)
    print(datetime.timedelta(days=30))
    print(date_debut_semaine)

    # filtrer les enregistrements créés depuis le début de la semaine dernière
    dht = Dht11.objects.filter(dt__gte=date_debut_semaine)

    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)

@login_required
def sendtele():
    token = '6662023260:AAG4z48OO9gL8A6szdxg0SOma5hv9gIII1E'
    rece_id = 1242839034
    bot = telepot.Bot(token)
    bot.sendMessage(rece_id, 'la température depasse la normale')
    print(bot.sendMessage(rece_id, 'OK.'))
