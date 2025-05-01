from django.urls import path
from . import views
from django.contrib import admin
from . import api
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register_view, name='register_view'),
    path("api",api.Dlist,name='json'),
    path("api/post",api.Dlist,name='json'),
    path('download_csv/', views.download_csv, name='download_csv'),
    path('index/',views.table,name='table'),
    path('graphiqueTemp/',views.graphiqueTemp,name='graphiqueTemp'),
    path('graphiqueHum/', views.graphiqueHum, name='graphiqueHum'),
    path('chart-data/', views.chart_data, name='chart-data'),

    path('chart-data-jour/',views.chart_data_jour,name='chart-data-jour'),
    path('chart-data-semaine/',views.chart_data_semaine,name='chart-data-semaine'),
    path('chart-data-mois/',views.chart_data_mois,name='chart-data-mois'),
    path('', views.home, name='home'),
    path('login_view/', views.login_view, name='login_view'),
    path('logout_view/', views.logout_view, name='logout_view'),

]